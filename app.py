"""GeoFo — serwer strony www.geofoapp.com.

Serwuje gotową stronę z folderu site/ (mapy, atlas, gry, quizy) i dodaje czat AI
przez /api/chat, jeśli ustawiony jest klucz ANTHROPIC_API_KEY.

Uruchomienie:
    pip install -r requirements.txt
    python app.py            ->  http://localhost:8080
"""
import os
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory

SITE = Path(__file__).parent / "site"
app = Flask(__name__, static_folder=None)

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5")
LEVELS = {
    "prosto": "Odpowiadaj bardzo prosto, krótko i przystępnie, jak dla ucznia szkoły podstawowej.",
    "normalnie": "Dopasuj długość do pytania: na proste krótko, na trudne rzetelnie z wyjaśnieniem.",
    "ekspert": "Odpowiadaj na poziomie akademickim: precyzyjne terminy, mechanizmy, liczby i kontekst naukowy.",
}
SYSTEM = (
    "Jesteś GeoBotem, asystentem strony GeoFo (www.geofoapp.com) o geografii. "
    "Odpowiadaj po polsku, chyba że użytkownik pisze w innym języku. "
    "Odpowiadasz na pytania z geografii na każdym poziomie: od prostych (stolice, kontynenty, rzeki) "
    "po bardzo zaawansowane (geomorfologia, klimatologia, kartografia, odwzorowania, GIS, tektonika, "
    "hydrologia, demografia). {level} Jeśli czegoś nie wiesz na pewno, powiedz to. "
    "Formatuj zwykłym tekstem; możesz używać **pogrubień**, list z myślnikami i nagłówków ###."
)


@app.get("/")
def index():
    return send_from_directory(SITE, "index.html")


@app.get("/config.js")
def config_js():
    """Klucz Mapy.com z zmiennej MAPY_API_KEY (zakładka "Mapy dokładne")."""
    key = os.environ.get("MAPY_API_KEY")
    if not key:
        return send_from_directory(SITE, "config.js")
    import json
    return app.response_class(f"window.GEOFO_MAPY_KEY = {json.dumps(key)};\n", mimetype="application/javascript")


@app.get("/<path:name>")
def files(name):
    if name.startswith("api/"):
        abort(404)
    return send_from_directory(SITE, name, max_age=86400)


@app.get("/api/status")
def status():
    return jsonify({"ai": bool(os.environ.get("ANTHROPIC_API_KEY"))})


@app.post("/api/chat")
def chat():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return jsonify({"code": "sampling_disabled"}), 503
    import anthropic

    body = request.get_json(force=True, silent=True) or {}
    msgs = [{"role": m["role"], "content": str(m["content"])[:4000]}
            for m in body.get("messages", [])[-12:]
            if m.get("role") in ("user", "assistant") and m.get("content")]
    while msgs and msgs[0]["role"] != "user":
        msgs.pop(0)
    if not msgs or msgs[-1]["role"] != "user":
        return jsonify({"code": "invalid_request"}), 400
    level = LEVELS.get(body.get("level"), LEVELS["normalnie"])
    try:
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(model=MODEL, max_tokens=1500,
                                      system=SYSTEM.format(level=level), messages=msgs)
        reply = "".join(b.text for b in resp.content if b.type == "text")
    except anthropic.RateLimitError:
        return jsonify({"code": "rate_limited"}), 429
    except Exception:  # noqa: BLE001
        app.logger.exception("Błąd czatu")
        return jsonify({"code": "upstream_error"}), 502
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
