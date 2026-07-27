import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src")
DATA = os.path.join(BASE, "data")
OUT_DIR = os.path.join(BASE, "dist")

parts = [
    "part1_head.html",
    "part2_body.html",
    "part3_script_top.html",
    "part3c_firebase.html",
    "part3b_ronde.html",
    "part4_teams.html",
    "part6_clubs.html",
    "part7_stats.html",
    "part8_beker.html",
    "part5_rest.html",
]

html = "\n".join(open(os.path.join(SRC, p), encoding="utf-8").read() for p in parts)

spelregels = json.load(open(os.path.join(DATA, "spelregels.json"), encoding="utf-8"))
players = json.load(open(os.path.join(DATA, "players.json"), encoding="utf-8"))
teams = json.load(open(os.path.join(DATA, "teams.json"), encoding="utf-8"))
allweeks = json.load(open(os.path.join(DATA, "allweeks.json"), encoding="utf-8"))
tussenstand = json.load(open(os.path.join(DATA, "tussenstand.json"), encoding="utf-8"))

# json.dumps() escaped niets: als er ooit een letterlijke "</script" in een dataveld terechtkomt
# (bijv. een spelersnaam of clubnaam die per ongeluk zo'n string bevat), zou de browser de inline
# <script>-tag daar voortijdig afsluiten en de rest van de pagina stukmaken. Door "</" in de JSON-tekst
# te vervangen door "<\/" (een geldige JSON/JS-escape die niets aan de waarde verandert) kan dat nooit
# meer gebeuren, wat build.py hiermee onafhankelijk maakt van hoe schoon de brondata toevallig is.
def dump(obj):
    encoded = json.dumps(obj).replace("</", "<\\/")
    # Permanente regressiecheck op alléén deze databrok (niet de hele pagina, die legitiem vol staat met
    # echte </script>-tags): als dump() ooit kapot raakt, moet de build hier vastlopen in plaats van
    # stilletjes een onveilige pagina op te leveren.
    assert "</script" not in encoded.lower(), "Geëscapete data bevat nog een onveilige \"</script\" — build.py's escaping is kapot."
    return encoded

html = html.replace("__SPELREGELS_JSON__", dump(spelregels))
html = html.replace("__CLUBS_JSON__", dump(players["clubs"]))
html = html.replace("__PLAYERS_JSON__", dump(players["players"]))
html = html.replace("__TEAMS_JSON__", dump(teams))
html = html.replace("__ALLWEEKS_JSON__", dump(allweeks))
html = html.replace("__TUSSENSTAND_JSON__", dump(tussenstand))

os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print("OK, bytes:", len(html), "->", out_path)
