#!/usr/bin/env python3
"""Leest alle songs/*.html en schrijft songs/index.json voor het overzicht.
Draai dit na het toevoegen of aanpassen van een song:  python3 maak_index.py"""
import json, re, pathlib, datetime

map_songs = pathlib.Path(__file__).parent / "songs"
items = []

# Datum van toevoegen: wordt onthouden in index.json, zodat een latere aanpassing
# van een song hem niet opnieuw "nieuw" maakt.
oud = {}
try:
    oud = {x["bestand"]: x.get("toegevoegd", "") for x in
           json.loads((map_songs / "index.json").read_text(encoding="utf-8"))}
except Exception:
    pass
vandaag = datetime.date.today().isoformat()

for f in sorted(map_songs.glob("*.html")):
    tekst = f.read_text(encoding="utf-8")
    meta = {}
    m = re.search(r"<meta>(.*?)</meta>", tekst, re.S | re.I)
    if m:
        for deel in m.group(1).split(";"):
            if ":" in deel:
                k, v = deel.split(":", 1)
                meta[k.strip().lower()] = v.strip()
    rest = tekst[m.end():] if m else tekst
    kopregel = next((r.strip() for r in rest.splitlines()
                     if r.strip() and not r.strip().lower().startswith(("<key>", "capo"))), "")
    # artiest: eerst het veld 'artiest:' in <meta>, anders het deel na het streepje in de kopregel
    # (werkt met - en met de langere streepjes – en —)
    delen = re.split(r"\s+-\s+|\s*[–—]\s*", kopregel, maxsplit=1)
    artiest = meta.get("artiest") or (delen[1] if len(delen) > 1 else "")
    k = re.search(r"<key>\{?([^<}]*)\}?</key>", tekst, re.I)
    # 1) 'toegevoegd: 2026-10-31' in <meta>  2) bekende datum uit de vorige index.json
    # 3) nieuwe song: vandaag (de allereerste keer: de datum van het bestand)
    toegevoegd = meta.get("toegevoegd") or oud.get(f.name)
    if not toegevoegd:
        if any(oud.values()):
            toegevoegd = vandaag
        else:
            toegevoegd = datetime.date.fromtimestamp(f.stat().st_mtime).isoformat()
    # taal: NL, FR of SP (ES wordt ook als SP herkend); leeg = Engels/overig
    taal = meta.get("taal", "").strip().upper()
    taal = {"ES": "SP", "NEDERLANDS": "NL", "FRANS": "FR", "SPAANS": "SP"}.get(taal, taal)
    items.append({
        "bestand": f.name,
        "titel": meta.get("titel") or f.stem,
        "artiest": artiest,
        "key": k.group(1).strip() if k else "",
        "repertoire": meta.get("repertoire", "").lower() in ("ja", "yes", "true", "1", "x", "waar"),
        "taal": taal,
        "toegevoegd": toegevoegd,
        "goed": meta.get("goed", "").lower() in ("ja", "yes", "true", "1", "x", "waar"),
    })

(map_songs / "index.json").write_text(
    json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(items)} song(s) in songs/index.json")
