# GeoFo 2.4.0 — www.geofoapp.com

Jedna strona o geografii, która działa na trzy sposoby:

| Gdzie | Co działa | Koszt |
|---|---|---|
| Link z Claude (przycisk „Udostępnij”) | wszystko, czat AI dla zalogowanych w Claude | 0 zł |
| Darmowy hosting (Netlify, GitHub Pages) – folder `site/` | mapy, atlas, gry, quizy | 0 zł |
| Serwer w Pythonie (`app.py`) z kluczem API | wszystko, czat AI dla każdego | płatne zapytania AI |

## Co jest na stronie
- **Start**: kręcący się globus 3D, kraj dnia.
- **Mapy topograficzne**: rzeźba terenu, wysokości i głębie, zdjęcie satelitarne.
- **Mapy kartograficzne**: mapa polityczna, kontynenty, mapa ogólnogeograficzna, mapa konturowa.
- Na mapach są stolice i miasta, rzeki i jeziora, siatka geograficzna, wyszukiwarka, pomiar odległości i skala. Granice wyostrzają się przy przybliżaniu.
- **Mapy dokładne**: szczegółowa mapa Mapy.com (podstawowa, turystyczna, zdjęcia lotnicze, zimowa) bezpośrednio w GeoFo, bez logowania i bez klucza.
- **Atlas krajów**: tabela 250 państw i terytoriów z sortowaniem i porównaniem dwóch krajów.
- **Gry i quizy**:
  - quiz z 10 200 pytaniami na trzech poziomach;
  - „Gdzie to jest?” na mapie;
  - flagi na czas i stolice na czas;
  - wyzwanie dnia i „Większy czy mniejszy?”;
  - punkty XP, poziomy, statystyki i 13 odznak.
- **Czat AI (GeoBot)**: trzy poziomy odpowiedzi, a kraje wymienione w odpowiedzi można od razu pokazać na mapie.

## Nowości w 2.4.0 — GeoFo jako aplikacja (PWA)
- GeoFo można **zainstalować** na Androidzie, iPhonie, Windowsie, Macu i Chromebooku: własna ikona, pełny ekran, działanie **bez internetu** (mapy, atlas, quizy, gry).
- Nowe pliki w `site/`: `manifest.webmanifest`, `sw.js` (praca offline), `icons/` (ikony i zrzuty ekranu).
- Kod strony jest w `src/app.html`; `python build_site.py` buduje z niego `site/index.html`.

### Jak zainstalować (po wrzuceniu folderu `site` na GitHub Pages)
- **Android / Chrome / Edge:** na stronie startowej pojawi się karta „Zainstaluj GeoFo” (albo menu przeglądarki → „Zainstaluj aplikację”).
- **iPhone / iPad:** w Safari: Udostępnij → „Do ekranu początkowego”.
- Instalacja działa tylko z adresu https (GitHub Pages, Netlify itp.), nie z pliku na dysku ani z podglądu w Claude.

### Do sklepów (opcjonalnie, później)
Gdy strona działa w internecie, wpisz jej adres na https://www.pwabuilder.com — wygeneruje paczki do Google Play, Microsoft Store i projekt na iOS.

## Nowości w 2.3.1
- Po kliknięciu kraju na mapie: **ludność kraju**, **gęstość zaludnienia**, **ludność stolicy** i **powierzchnia stolicy** (z rokiem danych).
- Dane: Wikipedia (listy państw i stolic według ludności i powierzchni), pobrane 18.10.2026 — źródła w `data/raw/`, skrypt `add_population.py`.

## Plik do otwarcia dwuklikiem
`python build_single.py` tworzy `GeoFo.html` — jeden plik z całą stroną (bez konta, bez instalowania).

## Nowości w 2.2.1
- **Mapy dokładne** pokazują mapę Mapy.com od razu, **bez logowania i bez klucza API** (oficjalne osadzanie mapy Mapy.com).
- Wyszukiwarka miejsc w tej zakładce korzysta z darmowego wyszukiwania OpenStreetMap.
- Klucz API jest teraz opcjonalny („Tryb zaawansowany”) — nie trzeba go nigdzie wpisywać.
- W podglądzie w Claude mapy z innych serwisów są blokowane; na stronie opublikowanej w internecie (np. Netlify) mapa działa od razu.

## Nowości w 2.2.0
- Nowa zakładka **Mapy dokładne** (między Mapami kartograficznymi a Atlasem krajów).

## Nowości w 2.1.0
- Wyzwanie dnia (5 pytań dziennie, seria dni) i gra „Większy czy mniejszy?”
- Warstwa „Dzień i noc” na mapach, pełny ekran, przycisk „Losowy kraj”
- Słowniczek 50 pojęć geograficznych w Atlasie
- Karta „Czy wiesz, że…”, statystyki gracza, przełącznik motywu, 3 nowe odznaki (razem 13)

## Sposób 1: darmowa strona w internecie (bez instalowania)
1. Załóż darmowe konto na https://app.netlify.com/signup.
2. Wejdź na https://app.netlify.com/drop i przeciągnij folder **`site`**.
3. W „Site configuration → Change site name” wpisz `geofoapp`. Adres to wtedy **geofoapp.netlify.app**.

## Sposób 2: serwer z czatem AI
```bash
pip install -r requirements.txt
# Windows:   set ANTHROPIC_API_KEY=twoj_klucz
# Mac/Linux: export ANTHROPIC_API_KEY=twoj_klucz
python app.py
```
Strona będzie pod http://localhost:8080. W internecie (Google Cloud Run):
```bash
echo -n "twoj_klucz" | gcloud secrets create anthropic-key --data-file=-
gcloud run deploy geofo --source . --region europe-central2 --allow-unauthenticated \
  --set-secrets ANTHROPIC_API_KEY=anthropic-key:latest
```
Domenę **geofoapp.com** kupuje się osobno, a potem podpina w Netlify albo w Cloud Run.

## Pliki
```
site/              gotowa strona (to wrzucasz na hosting)
app.py             serwer: serwuje site/ + czat AI (/api/chat)
quiz_generator.py  generator 10 200 pytań  -> data/questions.json
build_site.py      przenosi pytania do site/questions.json
data/              dane krajów, polskie nazwy stolic, języków i walut
```
Zmiana pytań: `python quiz_generator.py && python build_site.py`.

## Źródła danych
Granice: Natural Earth (world-atlas). Rzeźba terenu, ETOPO1, Blue Marble i rzeki: pakiet basemap-data (NASA/NOAA). Miasta: GeoNames. Kraje: mledoze/countries. Flagi: flag-icons.
