import sqlite3
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT, "data", "sentinel.db")
JSON_PATH = os.path.join(ROOT, "sentinel_all_31.json")

def import_cams():
    if not os.path.exists(JSON_PATH):
        print("JSON file not found.")
        return

    with open(JSON_PATH, "r") as f:
        cams = json.load(f)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    count = 0
    for c in cams:
        cid = f"cam-{c['id']}"
        name = f"Camera {c['id']} — {c.get('location', '')}"
        live_url = f"https://live.sentinelgujarat.in/camera/{c['id']}"
        spot = c.get('location', '')
        
        # Determine city mapping based on location text
        loc_lower = spot.lower()
        city_id = "surat"
        area_id = "athwa"
        lat, lng = 21.17, 72.83

        if "junagadh" in loc_lower:
            city_id = "junagadh"
            area_id = "city"
            lat, lng = 21.52, 70.46
        elif "rajkot" in loc_lower:
            city_id = "rajkot"
            area_id = "race"
            lat, lng = 22.30, 70.80
        elif "gandhidham" in loc_lower or "kutch" in loc_lower:
            city_id = "kutch"
            area_id = "gandhidham"
            lat, lng = 23.08, 70.13
        elif "patan" in loc_lower or "adalaj" in loc_lower:
            city_id = "gandhinagar"
            area_id = "infocity"
            lat, lng = 23.21, 72.63
        elif "chiman" in loc_lower or "janpath" in loc_lower or "paldi" in loc_lower or "visat" in loc_lower:
            city_id = "ahmedabad"
            area_id = "central"
            lat, lng = 23.02, 72.57

        cur.execute(
            """INSERT OR REPLACE INTO cameras 
               (id, name, place, lat, lng, source, kind, status, last_note, city_id, area_id, owner, spot, estate, live_url) 
               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                cid, name, city_id.title(), lat, lng, live_url, "live", "ready",
                f"Live Sentinel Gujarat Stream ({c.get('location')})",
                city_id, area_id, "Sentinel Gujarat Live", spot, 1, live_url
            )
        )
        count += 1

    con.commit()
    con.close()
    print(f"Successfully imported all {count} live camera feeds into SentinelShield database!")

if __name__ == "__main__":
    import_cams()
