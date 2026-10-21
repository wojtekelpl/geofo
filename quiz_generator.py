"""Generator pytań quizowych GeoFo.

Tworzy ok. 10 000 unikalnych pytań w trzech kategoriach: latwe, srednie, trudne.
Uruchom:  python quiz_generator.py   ->  zapisuje data/questions.json
"""
import json
import random
from pathlib import Path

BASE = Path(__file__).parent
TARGET_PER_LEVEL = 3400  # 3 x 3400 = 10 200 pytań

REGIONS = {"Europe": "Europa", "Asia": "Azja", "Africa": "Afryka", "Americas": "Ameryka",
           "Oceania": "Oceania", "Antarctic": "Antarktyka"}
SUBREGIONS = {
    "Northern Europe": "Europa Północna", "Western Europe": "Europa Zachodnia",
    "Southern Europe": "Europa Południowa", "Eastern Europe": "Europa Wschodnia",
    "Central Europe": "Europa Środkowa", "Southeast Europe": "Europa Południowo-Wschodnia",
    "Western Asia": "Azja Zachodnia", "Central Asia": "Azja Środkowa",
    "Southern Asia": "Azja Południowa", "Eastern Asia": "Azja Wschodnia",
    "South-Eastern Asia": "Azja Południowo-Wschodnia", "Northern Africa": "Afryka Północna",
    "Western Africa": "Afryka Zachodnia", "Eastern Africa": "Afryka Wschodnia",
    "Middle Africa": "Afryka Środkowa", "Southern Africa": "Afryka Południowa",
    "North America": "Ameryka Północna", "Central America": "Ameryka Środkowa",
    "South America": "Ameryka Południowa", "Caribbean": "Karaiby",
    "Australia and New Zealand": "Australia i Nowa Zelandia", "Melanesia": "Melanezja",
    "Micronesia": "Mikronezja", "Polynesia": "Polinezja",
}

# Ręcznie przygotowane pytania z geografii fizycznej
STATIC = [
    ("latwe", "Jaki jest najwyższy szczyt świata?", "Mount Everest", ["K2", "Mont Blanc", "Kilimandżaro"]),
    ("latwe", "Który ocean jest największy?", "Ocean Spokojny", ["Ocean Atlantycki", "Ocean Indyjski", "Ocean Arktyczny"]),
    ("latwe", "Jaka jest najdłuższa rzeka w Polsce?", "Wisła", ["Odra", "Warta", "Bug"]),
    ("latwe", "Jaki jest najwyższy szczyt Polski?", "Rysy", ["Śnieżka", "Babia Góra", "Giewont"]),
    ("latwe", "Na którym kontynencie leży Sahara?", "Afryka", ["Azja", "Australia", "Ameryka Południowa"]),
    ("latwe", "Ile jest kontynentów (w polskiej tradycji szkolnej)?", "7", ["5", "6", "8"]),
    ("latwe", "Które morze oblewa Polskę?", "Morze Bałtyckie", ["Morze Północne", "Morze Czarne", "Morze Śródziemne"]),
    ("latwe", "Jak nazywa się linia dzieląca Ziemię na półkulę północną i południową?", "Równik", ["Zwrotnik Raka", "Południk zerowy", "Koło podbiegunowe"]),
    ("srednie", "Która rzeka jest najdłuższa na świecie (wg większości źródeł)?", "Nil", ["Amazonka", "Jangcy", "Missisipi"]),
    ("srednie", "Jakie jest najgłębsze jezioro świata?", "Bajkał", ["Tanganika", "Morze Kaspijskie", "Wiktorii"]),
    ("srednie", "W jakich górach leży Mont Blanc?", "Alpy", ["Pireneje", "Karpaty", "Apeniny"]),
    ("srednie", "Jaka jest największa pustynia gorąca na świecie?", "Sahara", ["Gobi", "Kalahari", "Atakama"]),
    ("srednie", "Który kraj ma najwięcej stref czasowych (z terytoriami zależnymi)?", "Francja", ["Rosja", "USA", "Chiny"]),
    ("srednie", "Jak nazywa się największe jezioro w Polsce?", "Śniardwy", ["Mamry", "Hańcza", "Gopło"]),
    ("srednie", "Które jezioro w Polsce jest najgłębsze?", "Hańcza", ["Śniardwy", "Wigry", "Drawsko"]),
    ("srednie", "Jak nazywa się najwyższy szczyt Afryki?", "Kilimandżaro", ["Mount Kenya", "Ras Daszan", "Ruwenzori"]),
    ("srednie", "Przez który kontynent przechodzą zarówno równik, jak i oba zwrotniki?", "Afryka", ["Ameryka Południowa", "Azja", "Australia"]),
    ("srednie", "Jak nazywa się cieśnina oddzielająca Europę od Afryki?", "Cieśnina Gibraltarska", ["Bosfor", "Cieśnina Beringa", "Kanał La Manche"]),
    ("trudne", "Jak nazywa się najgłębsze miejsce oceanów?", "Głębia Challengera", ["Rów Puerto Rico", "Rów Tonga", "Głębia Sundajska"]),
    ("trudne", "Jaki jest najwyższy szczyt Ameryki Południowej?", "Aconcagua", ["Chimborazo", "Huascarán", "Ojos del Salado"]),
    ("trudne", "Który proces tworzy fiordy?", "Erozja lodowcowa", ["Erozja wiatrowa", "Wulkanizm", "Abrazja morska"]),
    ("trudne", "Jak nazywa się skala używana do pomiaru twardości minerałów?", "Skala Mohsa", ["Skala Richtera", "Skala Beauforta", "Skala Mercallego"]),
    ("trudne", "W której warstwie atmosfery zachodzą niemal wszystkie zjawiska pogodowe?", "Troposfera", ["Stratosfera", "Mezosfera", "Termosfera"]),
    ("trudne", "Jak nazywa się zjawisko okresowego ocieplenia wód wschodniego Pacyfiku?", "El Niño", ["La Niña", "Monsun", "Fen"]),
    ("trudne", "Jaka jest depresja położona najniżej na lądzie?", "Morze Martwe", ["Depresja Turfańska", "Dolina Śmierci", "Depresja Kattara"]),
    ("trudne", "Która płyta tektoniczna jest największa?", "Płyta pacyficzna", ["Płyta euroazjatycka", "Płyta afrykańska", "Płyta północnoamerykańska"]),
    ("trudne", "Jak nazywa się najniższy punkt w Polsce?", "Raczki Elbląskie", ["Żuławy Wiślane koło Gdańska", "Jezioro Łebsko", "Ujście Odry"]),
    ("trudne", "Na jakiej szerokości geograficznej leży Zwrotnik Koziorożca?", "ok. 23°26′ S", ["ok. 23°26′ N", "ok. 66°33′ S", "0°"]),
]


def fmt_area(a):
    return f"{int(round(a)):,}".replace(",", " ") + " km²"


class Gen:
    def __init__(self, countries, seed=42):
        self.rng = random.Random(seed)
        self.all = countries
        self.c = [c for c in countries if c["area"] and c["area"] > 0]
        self.by3 = {c["cca3"]: c for c in countries}
        self.indep = [c for c in self.c if c["independent"]]
        self.seen = set()
        self.out = {"latwe": [], "srednie": [], "trudne": []}

    def add(self, level, q, answer, wrong, category):
        wrong = list(dict.fromkeys(w for w in wrong if w and w != answer))[:3]
        if len(wrong) < 3 or q in self.seen or len(self.out[level]) >= TARGET_PER_LEVEL:
            return
        self.seen.add(q)
        opts = wrong + [answer]
        self.rng.shuffle(opts)
        self.out[level].append({"q": q, "options": opts, "answer": answer, "category": category})

    def others(self, pool, key, exclude, n=3):
        vals = list({key(x) for x in pool if key(x) and key(x) != exclude})
        self.rng.shuffle(vals)
        return vals[:n]

    def full(self, level):
        return len(self.out[level]) >= TARGET_PER_LEVEL

    def run(self):
        for lvl, q, a, w in STATIC:
            self.add(lvl, q, a, w, "Geografia fizyczna")
        R = self.rng

        # ---------- ŁATWE ----------
        for c in self.indep:
            if c["capital"]:
                same = [x for x in self.indep if x["region"] == c["region"] and x["capital"]]
                self.add("latwe", f"Jaka jest stolica państwa {c['name']}?", c["capital"][0],
                         self.others(same, lambda x: x["capital"][0], c["capital"][0]), "Stolice")
                self.add("latwe", f"Którego państwa stolicą jest {c['capital'][0]}?", c["name"],
                         self.others(same, lambda x: x["name"], c["name"]), "Stolice")
            self.add("latwe", f"Do którego państwa należy flaga {c['flag']}?", c["name"],
                     self.others([x for x in self.indep if x["region"] == c["region"]], lambda x: x["name"], c["name"]), "Flagi")
            self.add("latwe", f"Na jakim kontynencie / w jakim regionie leży {c['name']}?", REGIONS[c["region"]],
                     self.others(self.c, lambda x: REGIONS[x["region"]], REGIONS[c["region"]]), "Kontynenty")
            self.add("latwe", f"Jak wygląda flaga państwa {c['name']}?", c["flag"],
                     self.others([x for x in self.indep if x["region"] == c["region"]], lambda x: x["flag"], c["flag"]), "Flagi")
        # Porównania par dużych państw (łatwe: duża różnica powierzchni)
        big = sorted(self.indep, key=lambda x: -x["area"])[:120]
        pairs = [(a, b) for a in big for b in big if a is not b and a["area"] > 4 * b["area"]]
        R.shuffle(pairs)
        for a, b in pairs[:1200]:
            if self.full("latwe"):
                break
            pool = [x["name"] for x in R.sample(big, 6) if x["area"] < a["area"]]
            self.add("latwe", f"Które państwo ma największą powierzchnię: {a['name']}, {b['name']} czy inne z listy?",
                     a["name"], [b["name"]] + pool, "Powierzchnia")
        # Grupowe: który kraj leży na danym kontynencie
        for _ in range(20000):
            if self.full("latwe"):
                break
            c = R.choice(self.indep)
            others = [x["name"] for x in R.sample(self.indep, 12) if x["region"] != c["region"]]
            reg = REGIONS[c["region"]]
            wrong = others[:3]
            if len(wrong) == 3:
                q = f"Które państwo leży w regionie {reg}: {', '.join(sorted(wrong + [c['name']]))}?"
                self.add("latwe", q, c["name"], wrong, "Kontynenty")

        # ---------- ŚREDNIE ----------
        for c in self.c:
            if c["subregion"] in SUBREGIONS:
                self.add("srednie", f"W jakim subregionie świata leży {c['name']}?", SUBREGIONS[c["subregion"]],
                         self.others(self.c, lambda x: SUBREGIONS.get(x["subregion"]), SUBREGIONS[c["subregion"]]), "Regiony")
            generic = {"dolar", "frank", "funt", "peso", "rial", "dinar", "rupia", "szyling", "korona", "rubel", "kwacha", "euro"}
            sharp = lambda x: x["currencies"][0] if x["currencies"] and x["currencies"][0] not in generic else None
            if sharp(c) or (c["currencies"] and c["currencies"][0] == "euro"):
                self.add("srednie", f"Jaka waluta obowiązuje w państwie {c['name']}?", c["currencies"][0],
                         self.others(self.c, sharp, c["currencies"][0]), "Waluty")
            if c["languages"]:
                self.add("srednie", f"Który język jest językiem urzędowym w państwie {c['name']}?", c["languages"][0],
                         [l for l in self.others(self.c, lambda x: x["languages"][0] if x["languages"] else None, c["languages"][0], 8)
                          if l not in c["languages"]], "Języki")
            if c["capital"] and not c["independent"]:
                self.add("srednie", f"Jaka jest stolica (ośrodek administracyjny) terytorium {c['name']}?", c["capital"][0],
                         self.others(self.c, lambda x: x["capital"][0] if x["capital"] else None, c["capital"][0]), "Stolice")
            if c["borders"]:
                nb = self.by3[R.choice(c["borders"])]
                non = [x["name"] for x in self.c if x["cca3"] not in c["borders"] and x is not c and x["region"] == c["region"]]
                R.shuffle(non)
                self.add("srednie", f"Które z państw graniczy z państwem {c['name']}?", nb["name"], non, "Granice")
            if c["tld"]:
                self.add("srednie", f"Jaka jest internetowa domena krajowa państwa {c['name']}?", c["tld"][0],
                         self.others(self.c, lambda x: x["tld"][0] if x["tld"] else None, c["tld"][0]), "Kody")
        # Tak/Nie wymaga 3 błędnych odpowiedzi — zamieniamy na pytanie z wyborem
        for _ in range(30000):
            if self.full("srednie"):
                break
            land = [x for x in self.c if x["landlocked"]]
            sea = [x for x in self.c if not x["landlocked"]]
            if R.random() < 0.5:
                a = R.choice(land); w = [x["name"] for x in R.sample(sea, 3)]
                q = f"Które państwo NIE ma dostępu do morza: {', '.join(sorted(w + [a['name']]))}?"
            else:
                a = R.choice(sea); w = [x["name"] for x in R.sample(land, 3)]
                q = f"Które państwo MA dostęp do morza: {', '.join(sorted(w + [a['name']]))}?"
            self.add("srednie", q, a["name"], w, "Położenie")
            # Granice: pary
            c = R.choice([x for x in self.c if x["borders"]])
            nb = self.by3[R.choice(c["borders"])]
            non = [x["name"] for x in R.sample(self.c, 10) if x["cca3"] not in c["borders"] and x is not c]
            if len(non) >= 3:
                w = non[:3]
                q = f"Które państwo graniczy z państwem {c['name']}: {', '.join(sorted(w + [nb['name']]))}?"
                self.add("srednie", q, nb["name"], w, "Granice")

        # ---------- TRUDNE ----------
        for c in self.c:
            self.add("trudne", f"Jaki jest trzyliterowy kod ISO państwa {c['name']}?", c["cca3"],
                     self.others(self.c, lambda x: x["cca3"], c["cca3"]), "Kody")
            if c["calling"]:
                self.add("trudne", f"Jaki jest numer kierunkowy państwa {c['name']}?", c["calling"][0],
                         self.others(self.c, lambda x: x["calling"][0] if x["calling"] else None, c["calling"][0]), "Kody")
            n = len(c["borders"])
            self.add("trudne", f"Z iloma państwami graniczy {c['name']} (granice lądowe)?", str(n),
                     [str(v) for v in R.sample([k for k in range(0, 15) if k != n], 3)], "Granice")
            a = c["area"]
            wrong = [fmt_area(a * f) for f in R.sample([0.1, 0.25, 0.4, 2.5, 4, 10, 0.05, 20], 3)]
            self.add("trudne", f"Jaka jest przybliżona powierzchnia państwa {c['name']}?", fmt_area(a), wrong, "Powierzchnia")
        for _ in range(200000):
            if self.full("trudne"):
                break
            t = R.random()
            four = R.sample(self.indep, 4)
            names = sorted(x["name"] for x in four)
            if t < 0.3:
                ans = max(four, key=lambda x: x["latlng"][0])
                q = f"Które terytorium leży najdalej na północ: {', '.join(names)}?"
                cat = "Współrzędne"
            elif t < 0.55:
                ans = min(four, key=lambda x: x["latlng"][1])
                q = f"Które terytorium leży najdalej na zachód: {', '.join(names)}?"
                cat = "Współrzędne"
            elif t < 0.8:
                ans = max(four, key=lambda x: x["area"])
                q = f"Które ma największą powierzchnię: {', '.join(names)}?"
                cat = "Powierzchnia"
            else:
                ans = min(four, key=lambda x: x["area"])
                q = f"Które ma najmniejszą powierzchnię: {', '.join(names)}?"
                cat = "Powierzchnia"
            self.add("trudne", q, ans["name"], [x["name"] for x in four if x is not ans], cat)
        return self.out


def main():
    countries = json.loads((BASE / "data" / "countries.json").read_text(encoding="utf-8"))
    out = Gen(countries).run()
    (BASE / "data" / "questions.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    for k, v in out.items():
        print(k, len(v))
    print("Razem:", sum(len(v) for v in out.values()))


if __name__ == "__main__":
    main()
