"""Buduje folder site/ (uruchom po zmianie kodu, pytań lub danych).

    python quiz_generator.py   # nowe pytania -> data/questions.json
    python build_site.py       # site/questions.json + site/index.html (z src/app.html, z oznaczeniami aplikacji PWA)
"""
import json
import re
from pathlib import Path

BASE = Path(__file__).parent


def flag2code(s):
    return re.sub("[\U0001F1E6-\U0001F1FF]{2}",
                  lambda m: "⟦" + "".join(chr(ord(ch) - 0x1F1E6 + 65) for ch in m.group(0)) + "⟧", s)


def main():
    q = json.loads((BASE / "data" / "questions.json").read_text(encoding="utf-8"))
    cats = sorted({x["category"] for v in q.values() for x in v})
    out = {"cats": cats}
    for k, v in q.items():
        rows = []
        for x in v:
            t = flag2code(x["q"])
            if t.startswith("Do którego państwa należy flaga ⟦"):
                t = "Do którego państwa należy ta flaga? " + t[len("Do którego państwa należy flaga "):].rstrip("?")
            rows.append([t, [flag2code(o) for o in x["options"]], x["options"].index(x["answer"]), cats.index(x["category"])])
        out[k] = rows
    (BASE / "site" / "questions.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("site/questions.json:", sum(len(v) for k, v in out.items() if k != "cats"), "pytań")


HEAD = """<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="GeoFo: mapy topograficzne, kartograficzne i dokładne, atlas 250 państw z ludnością, quizy i gry z geografii.">
<meta name="theme-color" content="#0e2821">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="GeoFo">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""


def build_index():
    app = (BASE / "src" / "app.html").read_text(encoding="utf-8")
    (BASE / "site" / "index.html").write_text(HEAD + app + "\n</body>\n</html>\n", encoding="utf-8")
    print("site/index.html zbudowany z src/app.html")


if __name__ == "__main__":
    main()
    build_index()
