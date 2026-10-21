"""Buduje jeden plik GeoFo.html (wszystkie dane w środku), który otwiera się dwuklikiem.

    python build_single.py   ->  GeoFo.html

Bez kafelków wysokiej rozdzielczości (żeby plik nie był za duży).
Potrzebny jest internet tylko do: bibliotek (d3), czcionek, Map dokładnych (Mapy.com) i wyszukiwarki.
"""
import base64
import json
from pathlib import Path

BASE = Path(__file__).parent
SITE = BASE / "site"
JSON_FILES = ["countries.json", "borders.json", "borders-hd.json", "globe.json", "cities.json",
              "hydro.json", "flags.json", "questions.json"]
IMG_FILES = ["relief.jpg", "etopo.jpg", "sat.jpg", "hillshade.jpg"]


def main():
    page = (SITE / "index.html").read_text(encoding="utf-8")
    files = {n: (SITE / n).read_text(encoding="utf-8") for n in JSON_FILES}
    imgs = {n: "data:image/jpeg;base64," + base64.b64encode((SITE / n).read_bytes()).decode() for n in IMG_FILES}

    # images referenced from inline styles
    for n, uri in imgs.items():
        page = page.replace(f"url({n})", f"url({uri})")
    page = page.replace('"background-image:url(" + s.img + ")"', '"background-image:url(" + ((window.__GEOFO_IMG || {})[s.img] || s.img) + ")"')
    # no separate config file in the single-file version
    page = page.replace('<script src="config.js"></script>\n', "")

    shim = (
        "<script>\n"
        "// GeoFo single-file mode: serve embedded data instead of separate files\n"
        f"window.__GEOFO_FILES = {json.dumps(files, ensure_ascii=False)};\n"
        f"window.__GEOFO_IMG = {json.dumps(imgs)};\n"
        "(function () {\n"
        "  const F = window.__GEOFO_FILES, I = window.__GEOFO_IMG, of = window.fetch.bind(window);\n"
        "  window.fetch = (u, o) => { const k = String(u).split('?')[0].replace(/^\\.\\//, '');\n"
        "    if (F[k] != null) return Promise.resolve(new Response(F[k], {headers: {'Content-Type': 'application/json'}}));\n"
        "    if (k === 'api/status' || k === 'api/chat') return Promise.resolve(new Response('{}', {status: 404}));\n"
        "    return of(u, o); };\n"
        "  const d = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'src');\n"
        "  Object.defineProperty(HTMLImageElement.prototype, 'src', {get() { return d.get.call(this); },\n"
        "    set(v) { const k = String(v).replace(/^\\.\\//, ''); d.set.call(this, I[k] || v); }, configurable: true});\n"
        "})();\n"
        "</script>\n"
    )
    page = page.replace("<body>", "<body>" + shim, 1)
    out = BASE / "GeoFo.html"
    out.write_text(page, encoding="utf-8")
    print(out, round(out.stat().st_size / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
