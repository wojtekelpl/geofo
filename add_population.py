"""Dodaje do danych krajów: ludność kraju, ludność stolicy i powierzchnię stolicy.

Źródła (Wikipedia, pobrane 2026-10-18) są w data/raw/*.txt.
    python add_population.py   -> uzupełnia site/countries.json
"""
import json
import re
import unicodedata
from pathlib import Path

BASE = Path(__file__).parent
RAW = BASE / "data" / "raw"
ALIAS = {
    "democratic republic of the congo": "COD", "dr congo": "COD", "republic of the congo": "COG", "congo": "COG",
    "ivory coast": "CIV", "czech republic": "CZE", "east timor": "TLS", "timor-leste": "TLS",
    "micronesia": "FSM", "federated states of micronesia": "FSM", "the gambia": "GMB", "gambia": "GMB",
    "cape verde": "CPV", "vatican city": "VAT", "western sahara": "ESH", "hong kong": "HKG", "macau": "MAC",
    "us virgin islands": "VIR", "u.s. virgin islands": "VIR", "british virgin islands": "VGB", "aland": "ALA",
    "saint helena": "SHN", "saint helena, ascension and tristan da cunha": "SHN", "svalbard": "SJM",
    "south korea": "KOR", "north korea": "PRK", "russia": "RUS", "palestine": "PSE", "kosovo": "UNK",
    "eswatini": "SWZ", "north macedonia": "MKD", "sint maarten": "SXM", "saint martin": "MAF",
    "curacao": "CUW", "united states": "USA", "united kingdom": "GBR", "laos": "LAO", "syria": "SYR",
    "iran": "IRN", "vietnam": "VNM", "bolivia": "BOL", "venezuela": "VEN", "tanzania": "TZA", "moldova": "MDA",
    "brunei": "BRN", "taiwan": "TWN", "bahamas": "BHS", "cocos (keeling) islands": "CCK",
    "south georgia and the south sandwich islands": "SGS", "turkey": "TUR", "falkland islands": "FLK", "pitcairn islands": "PCN",
}


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s*\(.*?\)", "", s).strip()


def key(s):
    s = re.sub(r"\bst\.?\s", "saint ", norm(s))
    return re.sub(r"[^a-z]", "", s)


CAP_ALIAS = {"MNG": "Ulaanbaatar"}


def num(s):
    return float(s.replace(",", ""))


def rows(name):
    for line in (RAW / name).read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            yield line.split(";")


def main():
    raw = json.loads(Path("/tmp/wc/node_modules/world-countries/dist/countries.json").read_text()) \
        if Path("/tmp/wc/node_modules/world-countries/dist/countries.json").exists() else []
    names = dict(ALIAS)
    for c in raw:
        for n in [c["name"]["common"], c["name"]["official"], *c.get("altSpellings", [])]:
            names.setdefault(norm(n), c["cca3"])
    mine = json.loads((BASE / "data" / "countries.json").read_text(encoding="utf-8"))
    cap_en = {c["cca3"]: (c.get("capital_en") or [""])[0] for c in mine}

    def code(country):
        return names.get(norm(country))

    def cap_ok(cc, cap):
        b = key(cap)
        for name in (cap_en.get(cc, ""), CAP_ALIAS.get(cc, "")):
            a = key(name)
            if a and (a in b or b in a):
                return True
        return False

    out, miss = {}, []
    for country, p, date in rows("country_pop.txt"):
        cc = code(country)
        if not cc: miss.append(country); continue
        out.setdefault(cc, {})["p"] = int(num(p)); out[cc]["py"] = int(re.findall(r"\d{4}", date)[0])
    for country, cap, p, year in rows("capital_pop.txt"):
        cc = code(country)
        if not cc: miss.append(country); continue
        if cap_ok(cc, cap) and "cp" not in out.get(cc, {}):
            out.setdefault(cc, {}).update(cp=int(num(p)), cpy=int(year))
    for country, cap, a in rows("capital_area.txt"):
        cc = code(country)
        if not cc: miss.append(country); continue
        if cap_ok(cc, cap) and "ca" not in out.get(cc, {}):
            out.setdefault(cc, {})["ca"] = num(a)

    site = BASE / "site" / "countries.json"
    data = json.loads(site.read_text(encoding="utf-8"))
    for cc, v in data.items():
        for k in ("p", "py", "cp", "cpy", "ca"):
            v.pop(k, None)
        v.update(out.get(cc, {}))
    site.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    ind = [v for v in data.values() if v.get("ind")]
    print("bez dopasowania:", sorted(set(miss)))
    print("niepodległe:", len(ind), "z ludnością:", sum("p" in v for v in ind),
          "z ludnością stolicy:", sum("cp" in v for v in ind), "z pow. stolicy:", sum("ca" in v for v in ind))
    print("brak ludności stolicy:", sorted(v["n"] for v in ind if "cp" not in v))
    print("brak pow. stolicy:", sorted(v["n"] for v in ind if "ca" not in v))
    print("Polska:", {k: data["POL"].get(k) for k in ("p", "py", "cp", "cpy", "ca")})


if __name__ == "__main__":
    main()
