#!/usr/bin/env python3
"""Leest alle songs/*.html en schrijft songs/index.json voor het overzicht.
Draai dit na het toevoegen of aanpassen van een song:  python3 maak_index.py"""
import json, re, pathlib

map_songs = pathlib.Path(__file__).parent / "songs"
items = []

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
    kopregel = next((r.strip() for r in rest.splitlines() if r.strip()), "")
    artiest = kopregel.split(" - ", 1)[1] if " - " in kopregel else ""
    k = re.search(r"<key>\{?([^<}]*)\}?</key>", tekst, re.I)
    items.append({
        "bestand": f.name,
        "titel": meta.get("titel") or f.stem,
        "artiest": artiest,
        "key": k.group(1).strip() if k else "",
    })

(map_songs / "index.json").write_text(
    json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(items)} song(s) in songs/index.json")
