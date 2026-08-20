import sqlite3
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT, "data", "sentinel.db")

def clear_all_static():
    if not os.path.exists(DB_PATH):
        print("Database does not exist yet.")
        return

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    tables = [
        "watchlist",
        "sightings",
        "events",
        "alerts",
        "jobs",
        "hashes",
        "cyber",
        "evidence",
        "messages",
        "persons"
    ]

    for tbl in tables:
        cur.execute(f"DELETE FROM {tbl};")

    # Clear sample government registry cameras
    cur.execute("DELETE FROM cameras WHERE kind='registry' OR id LIKE 'gov-%';")

    con.commit()
    con.close()
    print("All static/demo data erased successfully!")

if __name__ == "__main__":
    clear_all_static()
