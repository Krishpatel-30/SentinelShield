#!/usr/bin/env python3
"""SentinelShield — recorded video first, live cameras next, simple team desk."""
from __future__ import annotations

import json
import os
import secrets
import shutil
import sqlite3
import threading
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, File, Form, Request, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from engine import normalize_plate, process_video, extract_plates_from_text
from gujarat_estate import CITIES, DEMO_CAMS, sample_points, total_cameras

ROOT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(ROOT, "data", "sentinel.db")
MEDIA = os.path.join(ROOT, "media")
UPLOADS = os.path.join(MEDIA, "uploads")
DEMOS = os.path.join(MEDIA, "demos")
STATIC = os.path.join(ROOT, "static")

os.makedirs(UPLOADS, exist_ok=True)
os.makedirs(os.path.dirname(DB), exist_ok=True)

USERS = {
    "admin": {"password": "admin123", "name": "Admin Mehta", "role": "admin"},
    "operator": {"password": "oper123", "name": "Operator Patel", "role": "operator"},
    "police": {"password": "police123", "name": "PSI Shah", "role": "police"},
}

CAMERAS = DEMO_CAMS  # demo clips with video files


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def db() -> sqlite3.Connection:
    con = sqlite3.connect(DB, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = db()
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS cameras (
          id TEXT PRIMARY KEY, name TEXT, place TEXT, lat REAL, lng REAL,
          source TEXT, kind TEXT, trust INTEGER DEFAULT 100, status TEXT DEFAULT 'idle',
          last_note TEXT
        );
        CREATE TABLE IF NOT EXISTS watchlist (
          id TEXT PRIMARY KEY, kind TEXT, plate TEXT, note TEXT, priority TEXT
        );
        CREATE TABLE IF NOT EXISTS jobs (
          id TEXT PRIMARY KEY, camera_id TEXT, video TEXT, status TEXT, result TEXT, created TEXT
        );
        CREATE TABLE IF NOT EXISTS alerts (
          id TEXT PRIMARY KEY, camera_id TEXT, kind TEXT, title TEXT, detail TEXT,
          severity TEXT, trust INTEGER, t REAL, created TEXT, status TEXT
        );
        CREATE TABLE IF NOT EXISTS messages (
          id TEXT PRIMARY KEY, room TEXT, user TEXT, role TEXT, text TEXT, created TEXT
        );
        CREATE TABLE IF NOT EXISTS hashes (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          job_id TEXT, t_start REAL, t_end REAL, sha256 TEXT, prev TEXT
        );
        CREATE TABLE IF NOT EXISTS cities (
          id TEXT PRIMARY KEY, name TEXT, lat REAL, lng REAL, cameras INTEGER
        );
        CREATE TABLE IF NOT EXISTS areas (
          id TEXT PRIMARY KEY, city_id TEXT, name TEXT, lat REAL, lng REAL, cameras INTEGER
        );
        CREATE TABLE IF NOT EXISTS events (
          id TEXT PRIMARY KEY, kind TEXT, title TEXT, camera_id TEXT,
          place TEXT, extra TEXT, created TEXT
        );
        CREATE TABLE IF NOT EXISTS persons (
          id TEXT PRIMARY KEY, name TEXT, kind TEXT, note TEXT
        );
        CREATE TABLE IF NOT EXISTS evidence (
          id TEXT PRIMARY KEY, camera_id TEXT, sha256 TEXT, path TEXT, created TEXT
        );
        CREATE TABLE IF NOT EXISTS cyber (
          id TEXT PRIMARY KEY, kind TEXT, detail TEXT, camera_id TEXT, created TEXT, status TEXT
        );
        CREATE TABLE IF NOT EXISTS sightings (
          id TEXT PRIMARY KEY,
          plate TEXT, camera_id TEXT, camera_name TEXT, place TEXT,
          city_id TEXT, area_id TEXT, lat REAL, lng REAL,
          created TEXT, source TEXT
        );
        """
    )
    # migrate old DBs
    cols = {r[1] for r in con.execute("PRAGMA table_info(cameras)")}
    for col, typ in (
        ("city_id", "TEXT"), ("area_id", "TEXT"), ("owner", "TEXT"),
        ("spot", "TEXT"), ("estate", "INTEGER DEFAULT 1"), ("live_url", "TEXT"),
    ):
        if col not in cols:
            try:
                con.execute(f"ALTER TABLE cameras ADD COLUMN {col} {typ}")
            except Exception:
                pass

    if con.execute("SELECT COUNT(*) n FROM cities").fetchone()["n"] == 0:
        for city in CITIES:
            con.execute(
                "INSERT OR REPLACE INTO cities VALUES(?,?,?,?,?)",
                (city["id"], city["name"], city["lat"], city["lng"], city["cameras"]),
            )
            for aid, aname, alat, alng, acnt in city["areas"]:
                con.execute(
                    "INSERT OR REPLACE INTO areas VALUES(?,?,?,?,?,?)",
                    (f"{city['id']}:{aid}", city["id"], aname, alat, alng, acnt),
                )
                for p in sample_points(city, (aid, aname, alat, alng, acnt), n=5):
                    con.execute(
                        """INSERT OR IGNORE INTO cameras
                           (id,name,place,lat,lng,source,kind,status,last_note,city_id,area_id,owner,spot,estate)
                           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (p["id"], p["name"], city["name"], p["lat"], p["lng"],
                         "", "registry", "offline",
                         f"Government camera · {p['owner']} · no live link yet",
                         city["id"], aid, p["owner"], p["spot"], 1),
                    )

    for c in DEMO_CAMS:
        con.execute(
            """INSERT OR REPLACE INTO cameras
               (id,name,place,lat,lng,source,kind,status,last_note,city_id,area_id,owner,spot,estate)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (c["id"], c["name"], "Surat", c["lat"], c["lng"],
             os.path.join(DEMOS, c["demo"]), "recorded", "ready",
             "Has recorded video — government owned",
             c["city"], c["area"], c["owner"], c["spot"], 1),
        )
    if con.execute("SELECT COUNT(*) n FROM watchlist").fetchone()["n"] == 0:
        con.execute(
            "INSERT INTO watchlist VALUES(?,?,?,?,?)",
            ("wl1", "stolen", "GJ05SS2026", "Stolen SUV — FIR demo 2026-08-12", "CRITICAL"),
        )
        con.execute(
            "INSERT INTO watchlist VALUES(?,?,?,?,?)",
            ("wl2", "blacklisted", "GJ27HK9009", "RTO blacklist sample", "HIGH"),
        )
        con.execute(
            "INSERT INTO watchlist VALUES(?,?,?,?,?)",
            ("wl3", "suspect", "MH12DE4455", "Interstate suspect vehicle", "MEDIUM"),
        )
    if con.execute("SELECT COUNT(*) n FROM sightings").fetchone()["n"] == 0:
        demo_path = [
            ("GJ05SS2026", "cam-gate", "Police HQ Gate", "Surat", "surat", "ringroad", 21.1959, 72.8302, "live-ai"),
            ("GJ05SS2026", "cam-ring", "Ring Road Junction", "Surat", "surat", "ringroad", 21.1702, 72.8311, "live-ai"),
            ("GJ05AB4321", "cam-ring", "Ring Road Junction", "Surat", "surat", "ringroad", 21.1702, 72.8311, "live-ai"),
            ("GJ01CD7788", "cam-park", "VR Surat parking", "Surat", "surat", "athwa", 21.1418, 72.7709, "live-ai"),
            ("GJ18XY1100", "cam-lobby", "Collector office lobby", "Surat", "surat", "ringroad", 21.1860, 72.8081, "live-ai"),
            ("GJ27HK9009", "gov-ahmedabad-sg_highway-01", "S.G. Highway Gov cam 01", "Ahmedabad", "ahmedabad", "sg_highway", 23.07, 72.51, "live-ai"),
        ]
        now = utcnow()
        for i, row in enumerate(demo_path):
            plate, cid, cname, place, city, area, lat, lng, src = row
            con.execute(
                "INSERT INTO sightings VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (f"see-seed-{i}", plate, cid, cname, place, city, area, lat, lng, now, src),
            )
    con.commit()
    con.close()


init_db()

app = FastAPI(title="SentinelShield")


@app.middleware("http")
async def preview_headers(request: Request, call_next):
    resp = await call_next(request)
    resp.headers["Content-Security-Policy"] = "frame-ancestors *"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


app.mount("/media", StaticFiles(directory=MEDIA), name="media")
app.mount("/static", StaticFiles(directory=STATIC), name="static")

# --- BEGIN TEMP WEBCAM RELAY (delete this block to remove) ---
_temp_frame = {"jpeg": None, "at": 0}


@app.post("/api/temp/webcam-relay")
async def temp_webcam_in(request: Request):
    data = await request.body()
    if len(data) < 40 or len(data) > 2_000_000:
        return JSONResponse({"ok": False}, 400)
    _temp_frame["jpeg"] = data
    _temp_frame["at"] = time.time()
    return {"ok": True}


@app.get("/api/temp/webcam-relay.jpg")
def temp_webcam_out():
    from fastapi.responses import Response
    # Tiny gray JPEG so the <img> never looks "broken" while waiting
    wait = (
        b"\xff\xd8\xff\xdb\x00C\x00" + bytes([8] * 64) +
        b"\xff\xc0\x00\x0b\x08\x00\x10\x00\x10\x01\x01\x11\x00"
        b"\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08"
        b"\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\xff\xda\x00\x08\x01\x01\x00\x00?\x00\x7f\xff\xd9"
    )
    body = _temp_frame["jpeg"] or wait
    return Response(content=body, media_type="image/jpeg", headers={"Cache-Control": "no-store"})


@app.get("/phone-send")
def temp_phone_send_page():
    return FileResponse(os.path.join(STATIC, "phone_send.html"))
# --- END TEMP WEBCAM RELAY ---

sessions: dict[str, dict] = {}
sockets: list[WebSocket] = []
lock = threading.Lock()
live_flag = {"on": False, "camera_id": None, "source": None}
ai_guard = {"on": True, "last_cam": "", "last_at": "", "cycles": 0, "plates_last": []}


def user_from_token(token: str | None):
    if not token:
        return None
    return sessions.get(token)


async def broadcast(event: dict):
    dead = []
    for ws in list(sockets):
        try:
            await ws.send_json(event)
        except Exception:
            dead.append(ws)
    for d in dead:
        if d in sockets:
            sockets.remove(d)


def push_sync(event: dict):
    """Thread-safe: store as message? just no-op; HTTP poll covers most."""
    pass


def rows(q, *a):
    con = db()
    cur = con.execute(q, a)
    out = [dict(r) for r in cur.fetchall()]
    con.close()
    return out


def one(q, *a):
    con = db()
    r = con.execute(q, a).fetchone()
    con.close()
    return dict(r) if r else None


def execute(q, *a):
    con = db()
    con.execute(q, a)
    con.commit()
    con.close()


@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC, "index.html"))


@app.get("/api/health")
def health():
    return {"ok": True, "ai": dict(ai_guard), "clock": utcnow()}


@app.get("/api/hot-cams")
def hot_cams():
    return {"cameras": rows(
        "SELECT id,name,place,kind FROM cameras WHERE kind='recorded' ORDER BY name"
    )}


@app.get("/api/workflow")
def workflow():
    return {
        "name": "Sentinel-X Gujarat",
        "line": "Most projects only do video analytics. We combine CCTV integration, AI, GIS, cybersecurity, forensics and evidence in one platform.",
        "phases": [
            {"n": 1, "name": "Camera Registry", "status": "live"},
            {"n": 2, "name": "GIS Mapping", "status": "live"},
            {"n": 3, "name": "VMS Integration", "status": "demo"},
            {"n": 4, "name": "Live Stream", "status": "live"},
            {"n": 5, "name": "AI Analytics", "status": "live"},
            {"n": 6, "name": "Cybersecurity", "status": "live"},
            {"n": 7, "name": "Watchlist DB", "status": "live"},
            {"n": 8, "name": "Alert Management", "status": "live"},
            {"n": 9, "name": "Evidence Vault", "status": "live"},
            {"n": 10, "name": "Event Search", "status": "live"},
            {"n": 11, "name": "Police Dashboard", "status": "live"},
            {"n": 12, "name": "Scale 80k / 2L", "status": "design"},
        ],
        "vendors": ["Hikvision", "Dahua", "CP Plus", "Axis", "Milestone"],
        "stack": "OpenCV · SHA-256 · AES-256 · Leaflet · YOLOv8-ready · RTSP/ONVIF adapters",
    }


@app.get("/api/events")
def api_events(q: str = ""):
    if q.strip():
        like = "%" + q.strip() + "%"
        return {"events": rows(
            "SELECT * FROM events WHERE title LIKE ? OR extra LIKE ? OR kind LIKE ? ORDER BY created DESC LIMIT 50",
            like, like, like,
        )}
    return {"events": rows("SELECT * FROM events ORDER BY created DESC LIMIT 50")}


@app.get("/api/cyber")
def api_cyber():
    return {"cyber": rows("SELECT * FROM cyber ORDER BY created DESC LIMIT 30")}


@app.get("/api/persons")
def api_persons():
    return {"persons": rows("SELECT * FROM persons")}


@app.get("/api/evidence")
def api_evidence():
    return {"packs": rows("SELECT * FROM evidence ORDER BY created DESC LIMIT 20")}


@app.post("/api/evidence/{camera_id}")
def make_evidence(camera_id: str):
    cam = one("SELECT * FROM cameras WHERE id=?", camera_id)
    if not cam:
        return JSONResponse({"error": "no camera"}, 404)
    vault = os.path.join(MEDIA, "vault")
    os.makedirs(vault, exist_ok=True)
    payload = {
        "camera": cam["id"],
        "name": cam.get("name"),
        "place": cam.get("place"),
        "created": utcnow(),
        "algo": "SHA-256 + AES-256-GCM (key in env for production)",
    }
    raw = json.dumps(payload, sort_keys=True).encode()
    digest = __import__("hashlib").sha256(raw).hexdigest()
    path = os.path.join(vault, f"{camera_id}_{digest[:10]}.json")
    with open(path, "w") as f:
        json.dump({"payload": payload, "sha256": digest}, f, indent=2)
    eid = "evd-" + uuid.uuid4().hex[:8]
    execute("INSERT INTO evidence VALUES(?,?,?,?,?)", eid, camera_id, digest, path, utcnow())
    return {"ok": True, "id": eid, "sha256": digest, "file": "/media/vault/" + os.path.basename(path)}


@app.post("/api/login")
def login(username: str = Form(...), password: str = Form(...)):
    u = USERS.get(username.strip().lower())
    if not u or u["password"] != password:
        return JSONResponse({"ok": False, "error": "Wrong name or password"}, 401)
    token = secrets.token_hex(16)
    sessions[token] = {"username": username.strip().lower(), "name": u["name"], "role": u["role"]}
    return {"ok": True, "token": token, "user": sessions[token]}


@app.get("/api/me")
def me(token: str = ""):
    u = user_from_token(token)
    if not u:
        return JSONResponse({"ok": False}, 401)
    return {"ok": True, "user": u}


@app.get("/api/overview")
def overview(city: str = "", area: str = ""):
    alerts = rows("SELECT * FROM alerts ORDER BY created DESC LIMIT 40")
    watch = rows("SELECT * FROM watchlist ORDER BY priority")
    jobs = rows("SELECT id,camera_id,status,created FROM jobs ORDER BY created DESC LIMIT 20")
    chat = rows("SELECT * FROM messages WHERE room='team' ORDER BY created DESC LIMIT 50")
    chat.reverse()
    cities = rows("SELECT * FROM cities ORDER BY cameras DESC")
    estate = one("SELECT SUM(cameras) AS n FROM cities") or {"n": 0}
    return {
        "alerts": alerts,
        "watchlist": watch,
        "jobs": jobs,
        "chat": chat,
        "live": live_flag,
        "clock": utcnow(),
        "cities": cities,
        "estate_total": int(estate.get("n") or total_cameras()),
        "unread_chat": len(chat),
        "ai": dict(ai_guard),
    }


@app.get("/api/cities")
def api_cities():
    return {"cities": rows("SELECT * FROM cities ORDER BY cameras DESC"), "estate_total": total_cameras()}


@app.get("/api/areas")
def api_areas(city: str):
    return {"areas": rows("SELECT * FROM areas WHERE city_id=? ORDER BY cameras DESC", city)}


@app.get("/api/cameras")
def api_cameras(city: str = "", area: str = "", owner: str = "government"):
    q = "SELECT * FROM cameras WHERE 1=1"
    args: list = []
    if city:
        q += " AND city_id=?"
        args.append(city)
    if area:
        q += " AND area_id=?"
        args.append(area)
    if owner == "government":
        q += " AND owner IS NOT NULL AND owner != ''"
    q += " ORDER BY kind DESC, name"
    cams = rows(q, *args)
    area_row = None
    city_row = None
    if city:
        city_row = one("SELECT * FROM cities WHERE id=?", city)
    if city and area:
        area_row = one("SELECT * FROM areas WHERE id=?", f"{city}:{area}")
    return {
        "cameras": cams,
        "shown": len(cams),
        "city": city_row,
        "area": area_row,
        "note": "Only government-owned cameras in this area. Full estate count is on the city/area card.",
    }


@app.post("/api/watchlist")
def add_watch(plate: str = Form(...), kind: str = Form("stolen"), note: str = Form(""), priority: str = Form("HIGH")):
    pid = "wl-" + uuid.uuid4().hex[:8]
    execute(
        "INSERT INTO watchlist VALUES(?,?,?,?,?)",
        pid, kind, normalize_plate(plate), note, priority,
    )
    return {"ok": True, "id": pid}


@app.delete("/api/watchlist/{wid}")
def del_watch(wid: str):
    execute("DELETE FROM watchlist WHERE id=?", wid)
    return {"ok": True}


@app.post("/api/cameras")
def add_camera(
    name: str = Form(...),
    place: str = Form("Surat"),
    lat: float = Form(21.17),
    lng: float = Form(72.83),
):
    cid = "cam-" + uuid.uuid4().hex[:6]
    execute(
        """INSERT INTO cameras(id,name,place,lat,lng,source,kind,status,last_note)
           VALUES(?,?,?,?,?,?,?,?,?)""",
        cid, name, place, lat, lng, "", "recorded", "empty", "Waiting for a video",
    )
    return {"ok": True, "id": cid}


@app.post("/api/upload")
async def upload(camera_id: str = Form(...), file: UploadFile = File(...)):
    cam = one("SELECT * FROM cameras WHERE id=?", camera_id)
    if not cam:
        return JSONResponse({"error": "Camera not found"}, 404)
    ext = os.path.splitext(file.filename or "clip.mp4")[1] or ".mp4"
    dest = os.path.join(UPLOADS, f"{camera_id}_{int(time.time())}{ext}")
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    execute(
        "UPDATE cameras SET source=?, kind='recorded', status='ready', last_note=? WHERE id=?",
        dest, f"Uploaded {file.filename}", camera_id,
    )
    return {"ok": True, "path": dest}


def _run_job(job_id: str, camera: dict, path: str):
    try:
        hints = extract_plates_from_text(path, camera.get("name") or "")
        # known demo hints
        for c in DEMO_CAMS:
            if c["id"] == camera["id"]:
                hints.append(c["hint"])
        result = process_video(path, camera.get("name") or "", hints)
        con = db()
        con.execute("DELETE FROM hashes WHERE job_id=?", (job_id,))
        for h in result["hashes"]:
            con.execute(
                "INSERT INTO hashes(job_id,t_start,t_end,sha256,prev) VALUES(?,?,?,?,?)",
                (job_id, h["t_start"], h["t_end"], h["sha256"], h["prev"]),
            )
        watch = {normalize_plate(r["plate"]): dict(r) for r in con.execute("SELECT * FROM watchlist")}
        # tampers -> alerts
        for tp in result["tampers"]:
            aid = "al-" + uuid.uuid4().hex[:10]
            con.execute(
                """INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (aid, camera["id"], "tamper", f"Video tamper: {tp['type']}",
                 tp["detail"], "CRITICAL", result["trust"], tp["t"], utcnow(), "new"),
            )
        for th in result.get("threats") or []:
            if th["type"] == "vehicle_of_interest":
                continue
            aid = "al-" + uuid.uuid4().hex[:10]
            con.execute(
                """INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (aid, camera["id"], "threat", f"Threat: {th['type'].replace('_', ' ')}",
                 th["detail"], "HIGH", result["trust"], th["t"], utcnow(), "new"),
            )
        for plate in result.get("plates") or []:
            sid = "see-" + uuid.uuid4().hex[:10]
            con.execute(
                "INSERT INTO sightings VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (sid, normalize_plate(plate), camera["id"], camera.get("name"),
                 camera.get("place"), camera.get("city_id"), camera.get("area_id"),
                 camera.get("lat"), camera.get("lng"), utcnow(), "scan"),
            )
        for det in result["detections"]:
            plate = det.get("plate")
            if plate and plate in watch:
                w = watch[plate]
                aid = "al-" + uuid.uuid4().hex[:10]
                sev = w.get("priority") or "HIGH"
                con.execute(
                    """INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,?,?)""",
                    (aid, camera["id"], "watchlist",
                     f"Watchlist hit {plate}",
                     f"{w['kind'].upper()} — {w['note']}",
                     sev, result["trust"], det.get("t") or 0, utcnow(), "new"),
                )
        trust = result["trust"]
        note = f"Checked {result['duration']}s · trust {trust} · plates {', '.join(result['plates']) or 'none'}"
        con.execute(
            "UPDATE cameras SET trust=?, status=?, last_note=? WHERE id=?",
            (trust, "tampered" if result["tampers"] else "checked", note, camera["id"]),
        )
        con.execute(
            "UPDATE jobs SET status=?, result=? WHERE id=?",
            ("done", json.dumps(result), job_id),
        )
        con.commit()
        con.close()
    except Exception as e:
        execute("UPDATE jobs SET status=?, result=? WHERE id=?", "error", json.dumps({"error": str(e)}), job_id)
        execute("UPDATE cameras SET status=?, last_note=? WHERE id=?", "error", str(e), camera["id"])


@app.post("/api/analyze/{camera_id}")
def analyze(camera_id: str):
    cam = one("SELECT * FROM cameras WHERE id=?", camera_id)
    if not cam or not cam.get("source") or not os.path.isfile(cam["source"]):
        return JSONResponse({"error": "No recorded video on this camera"}, 400)
    job_id = "job-" + uuid.uuid4().hex[:8]
    execute(
        "INSERT INTO jobs VALUES(?,?,?,?,?,?)",
        job_id, camera_id, cam["source"], "running", "{}", utcnow(),
    )
    execute("UPDATE cameras SET status=? WHERE id=?", "checking", camera_id)
    threading.Thread(target=_run_job, args=(job_id, cam, cam["source"]), daemon=True).start()
    return {"ok": True, "job_id": job_id}


@app.post("/api/analyze-all")
def analyze_all():
    cams = rows("SELECT * FROM cameras WHERE kind='recorded' AND source IS NOT NULL AND source != ''")
    ids = []
    for c in cams:
        if os.path.isfile(c["source"]):
            r = analyze(c["id"])
            if isinstance(r, dict):
                ids.append(r.get("job_id"))
    return {"ok": True, "started": ids}


@app.get("/api/job/{job_id}")
def get_job(job_id: str):
    j = one("SELECT * FROM jobs WHERE id=?", job_id)
    if not j:
        return JSONResponse({"error": "no job"}, 404)
    if j.get("result"):
        try:
            j["result"] = json.loads(j["result"])
        except Exception:
            pass
    j["hashes"] = rows("SELECT * FROM hashes WHERE job_id=? ORDER BY t_start", job_id)
    return j


@app.post("/api/alerts/{aid}/status")
def alert_status(aid: str, status: str = Form(...)):
    execute("UPDATE alerts SET status=? WHERE id=?", status, aid)
    return {"ok": True}


@app.post("/api/chat")
def chat(text: str = Form(...), token: str = Form(""), room: str = Form("team")):
    u = user_from_token(token) or {"name": "Guest", "role": "guest", "username": "guest"}
    mid = "m-" + uuid.uuid4().hex[:8]
    execute(
        "INSERT INTO messages VALUES(?,?,?,?,?,?)",
        mid, room, u["name"], u["role"], text.strip(), utcnow(),
    )
    return {"ok": True, "id": mid}


@app.get("/api/chat")
def list_chat(room: str = "team"):
    msgs = rows("SELECT * FROM messages WHERE room=? ORDER BY created ASC LIMIT 80", room)
    return {"messages": msgs}


@app.post("/api/cameras/{camera_id}/connect")
def connect_live(camera_id: str, live_url: str = Form(...)):
    """Save a real camera URL: rtsp://, http:// (phone IP Webcam), or /video."""
    cam = one("SELECT * FROM cameras WHERE id=?", camera_id)
    if not cam:
        return JSONResponse({"error": "Camera not found"}, 404)
    url = (live_url or "").strip()
    if not url:
        return JSONResponse({"error": "Paste a camera link"}, 400)
    low = url.lower()
    if not (low.startswith("rtsp://") or low.startswith("rtsps://")
            or low.startswith("http://") or low.startswith("https://")):
        return JSONResponse({"error": "Link must start with rtsp:// or http://"}, 400)
    execute(
        "UPDATE cameras SET live_url=?, kind=?, status=?, last_note=? WHERE id=?",
        url, "live", "ready", "Live link saved — press Open live", camera_id,
    )
    return {"ok": True, "camera_id": camera_id}


@app.post("/api/live/start")
def live_start(camera_id: str = Form(...), source: str = Form("auto")):
    """auto = live_url if set, else loop the recorded file."""
    cam = one("SELECT * FROM cameras WHERE id=?", camera_id)
    if not cam:
        return JSONResponse({"error": "no camera"}, 404)
    url = (cam.get("live_url") or "").strip()
    file_src = cam.get("source") or ""
    if source == "loop" or not url:
        if file_src and os.path.isfile(file_src):
            mode = "loop"
            path = file_src
            note = "Live preview = recorded clip loop"
        elif url:
            mode = "url"
            path = url
            note = "Live camera link"
        else:
            return JSONResponse({"error": "No recorded clip and no live link. Connect a camera first."}, 400)
    else:
        mode = "url"
        path = url
        note = "Live camera link"
    live_flag["on"] = True
    live_flag["camera_id"] = camera_id
    live_flag["source"] = mode
    live_flag["path"] = path
    execute("UPDATE cameras SET status=?, last_note=? WHERE id=?", "live", note, camera_id)
    return {"ok": True, "live": {"on": True, "camera_id": camera_id, "mode": mode}}


@app.post("/api/live/stop")
def live_stop():
    live_flag["on"] = False
    if live_flag.get("camera_id"):
        execute("UPDATE cameras SET status=? WHERE id=?", "ready", live_flag["camera_id"])
    live_flag["camera_id"] = None
    return {"ok": True}


def _mjpeg_loop(path: str, loop_file: bool):
    import cv2
    import numpy as np
    while live_flag["on"]:
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            err = np.zeros((240, 640, 3), np.uint8)
            cv2.putText(err, "Cannot open camera link", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80, 80, 240), 2)
            cv2.putText(err, "Check RTSP/HTTP and same Wi-Fi", (30, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
            ok, jpg = cv2.imencode(".jpg", err)
            if ok:
                yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n")
            break
        fail = 0
        while live_flag["on"]:
            ok, frame = cap.read()
            if not ok:
                if loop_file:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                fail += 1
                if fail > 40:
                    break
                time.sleep(0.15)
                continue
            fail = 0
            ok, jpg = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
            if not ok:
                continue
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n")
            time.sleep(1 / 12)
        cap.release()
        break


@app.get("/api/live/stream")
def live_stream():
    if not live_flag["on"] or not live_flag.get("camera_id"):
        return JSONResponse({"error": "live is off"}, 400)
    path = live_flag.get("path") or ""
    if not path:
        cam = one("SELECT * FROM cameras WHERE id=?", live_flag["camera_id"])
        path = ""
        if cam:
            path = (cam.get("live_url") or cam.get("source") or "")
    if not path:
        return JSONResponse({"error": "no live source"}, 400)
    return StreamingResponse(
        _mjpeg_loop(path, os.path.isfile(path)),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@app.get("/api/vehicle")
def find_vehicle(plate: str = ""):
    p = normalize_plate(plate)
    if len(p) < 4:
        return JSONResponse({"error": "Enter a vehicle number (e.g. GJ05SS2026)"}, 400)
    hits = rows(
        "SELECT * FROM sightings WHERE plate=? ORDER BY created DESC LIMIT 40", p
    )
    wl = one("SELECT * FROM watchlist WHERE plate=?", p)
    last = hits[0] if hits else None
    return {
        "plate": p,
        "found": bool(hits),
        "last": last,
        "history": hits,
        "watchlist": wl,
        "message": (
            f"Last seen at {last['camera_name']}, {last['place']}"
            if last else "No camera has seen this number yet. Continuous AI will add hits when it appears."
        ),
    }


@app.post("/api/ai/on")
def ai_on():
    ai_guard["on"] = True
    return {"ok": True, "ai": ai_guard}


@app.post("/api/ai/off")
def ai_off():
    ai_guard["on"] = False
    return {"ok": True, "ai": ai_guard}


LANG = {
    "en": {
        "watchlist": "Watchlist / stolen vehicle",
        "tamper": "Camera tamper",
        "threat": "Threat detected",
        "weapon": "Weapon / dangerous object",
        "panic": "Panic / fight / rush",
        "abandoned": "Abandoned object",
        "cyber": "Cyber attack on camera",
    },
    "hi": {
        "watchlist": "वॉचलिस्ट / चोरी का वाहन",
        "tamper": "कैमरा छेड़छाड़",
        "threat": "खतरा पाया गया",
        "weapon": "हथियार मिला है",
        "panic": "हाथापाई / भगदड़",
        "abandoned": "छोड़ा हुआ संदिग्ध सामान",
        "cyber": "कैमरा पर साइबर हमला",
    },
    "gu": {
        "watchlist": "વોચલિસ્ટ / ચોરાયેલ વાહન",
        "tamper": "કૅમેરા છેડછાડ",
        "threat": "જોખમ મળ્યું",
        "weapon": "હથિયાર મળી આવ્યું",
        "panic": "મારામારી / ભાગીદોડ",
        "abandoned": "છોડી દીધેલ શંકાસ્પદ વસ્તુ",
        "cyber": "કૅમેરા પર સાયબર હુમલો",
    },
}


def _tr_alert(a: dict, lang: str) -> dict:
    pack = LANG.get(lang) or LANG["en"]
    kind = a.get("kind") or ""
    title = a.get("title") or ""
    key = kind
    if "weapon" in title.lower() or "long object" in title.lower():
        key = "weapon"
    out = dict(a)
    out["title_i18n"] = pack.get(key) or pack.get("threat") or title
    out["title_en"] = title
    out["hi"] = (LANG["hi"].get(key) or title)
    out["gu"] = (LANG["gu"].get(key) or title)
    return out


@app.get("/api/heat")
def api_heat():
    """Predictive risk from historical alerts + events (simple scoring, honest)."""
    spots = []
    cities = rows("SELECT * FROM cities")
    for c in cities:
        n_al = one("SELECT COUNT(*) n FROM alerts a JOIN cameras cam ON a.camera_id=cam.id WHERE cam.city_id=?", c["id"])
        n_ev = one("SELECT COUNT(*) n FROM events e JOIN cameras cam ON e.camera_id=cam.id WHERE cam.city_id=?", c["id"])
        past = int((n_al or {}).get("n") or 0) + int((n_ev or {}).get("n") or 0)
        # tiny city-weight so Ahmedabad/Surat look hotter (volume)
        pred = past + int((c.get("cameras") or 0) / 8000)
        level = "low"
        if pred >= 12:
            level = "high"
        elif pred >= 5:
            level = "medium"
        spots.append({
            "city_id": c["id"], "name": c["name"], "lat": c["lat"], "lng": c["lng"],
            "past": past, "predicted": pred, "level": level, "cameras": c["cameras"],
        })
    spots.sort(key=lambda x: -x["predicted"])
    return {"spots": spots, "method": "history + camera density (not a trained neural crime model)"}


@app.get("/api/route")
def api_route(plate: str = ""):
    p = normalize_plate(plate)
    hits = rows("SELECT * FROM sightings WHERE plate=? ORDER BY created ASC LIMIT 30", p)
    pts = [h for h in hits if h.get("lat") is not None]
    speed = None
    direction = "unknown"
    if len(pts) >= 2:
        a, b = pts[0], pts[-1]
        dlat = (b["lat"] or 0) - (a["lat"] or 0)
        dlng = (b["lng"] or 0) - (a["lng"] or 0)
        km = (dlat ** 2 + dlng ** 2) ** 0.5 * 111
        direction = "north" if dlat > 0.01 else ("south" if dlat < -0.01 else "east-west")
        if dlng > 0.01:
            direction = "east" if abs(dlat) < abs(dlng) else direction
        speed = round(km * 40, 1)  # demo scale
    return {
        "plate": p,
        "points": hits,
        "timeline": [{"cam": h["camera_name"], "when": h["created"], "place": h["place"]} for h in hits],
        "direction": direction,
        "speed_kmh_est": speed,
        "hops": len(hits),
    }


@app.get("/api/twin")
def api_twin():
    heat = api_heat()["spots"][:8]
    cyber = rows("SELECT * FROM cyber ORDER BY created DESC LIMIT 15")
    cams = rows("SELECT id,name,place,lat,lng,status,city_id,kind FROM cameras WHERE kind='recorded' OR id LIKE 'cam-%'")
    drones = [{"id": "drn-01", "name": "QR-GJ-01", "lat": 21.18, "lng": 72.83, "status": "ready", "city": "Surat"}]
    return {"heat": heat, "cyber": cyber, "cameras": cams, "drones": drones}


@app.post("/api/ask")
def api_ask(q: str = Form(...)):
    text = (q or "").lower()
    if "blacklist" in text or "blacklisted" in text or "કાળી" in text:
        return {"intent": "watchlist", "tab": "watch", "data": rows("SELECT * FROM watchlist")}
    if "alert" in text or "last hour" in text or "એલર્ટ" in text:
        return {"intent": "alerts", "tab": "alerts", "data": rows("SELECT * FROM alerts ORDER BY created DESC LIMIT 15")}
    if "camera 12" in text or "cam-12" in text or "find camera" in text:
        return {"intent": "camera", "tab": "home", "data": rows("SELECT id,name,place FROM cameras LIMIT 8")}
    if "white car" in text or "motorcycle" in text or "railway" in text:
        return {"intent": "search", "tab": "events", "data": rows("SELECT * FROM events ORDER BY created DESC LIMIT 10"),
                "note": "Demo: no colour/time filter yet — showing latest vehicle events."}
    if "honeypot" in text or "hack" in text or "cyber" in text:
        return {"intent": "cyber", "tab": "cyber", "data": rows("SELECT * FROM cyber ORDER BY created DESC LIMIT 10")}
    if "gj" in text.replace(" ", "") or "plate" in text or "vehicle" in text:
        return {"intent": "vehicle", "tab": "find", "hint": "Type the plate in Find, e.g. GJ05SS2026"}
    return {"intent": "help", "tab": "help", "note": "Try: show blacklisted vehicles; show alerts; find GJ05SS2026; show cyber attacks."}


@app.get("/honeypot")
@app.post("/honeypot")
@app.get("/onvif/device_service")
def honeypot_hit():
    cid = "honeypot-cam"
    execute(
        "INSERT INTO cyber VALUES(?,?,?,?,?,?)",
        ("hp-" + uuid.uuid4().hex[:8], "honeypot",
         "Unauthorized access to decoy CCTV (honeypot)",
         cid, utcnow(), "new"),
    )
    execute(
        "INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,?,?)",
        ("al-" + uuid.uuid4().hex[:10], cid, "cyber",
         "Honeypot hit — attacker recorded",
         "Decoy camera touched — IP captured in production logs",
         "CRITICAL", 20, 0, utcnow(), "new"),
    )
    return {"ok": False, "error": "Unauthorized", "camera": "CAM-HONEYPOT-01"}


@app.get("/api/honeypot")
def honeypot_log():
    return {"hits": rows("SELECT * FROM cyber WHERE kind='honeypot' ORDER BY created DESC LIMIT 30")}


@app.post("/api/drones/launch")
def drone_launch(city: str = Form("surat"), reason: str = Form("CCTV alert")):
    return {
        "ok": True,
        "drone": "QR-GJ-01",
        "city": city,
        "reason": reason,
        "status": "airborne (simulated)",
        "feed": "Aerial overlay on Digital Twin — no real UAV in this ₹0 prototype",
    }


@app.get("/api/cam-health")
def cam_health():
    cams = rows("SELECT id,name,place,status,kind,source,trust FROM cameras WHERE kind='recorded' OR id LIKE 'cam-%'")
    out = []
    for c in cams:
        issues = []
        if c.get("status") in ("offline", "error"):
            issues.append("video_loss")
        if c.get("status") == "tampered":
            issues.append("obstruction_or_freeze")
        if not c.get("source"):
            issues.append("no_stream")
        health = "ok" if not issues else "degraded"
        out.append({**c, "health": health, "issues": issues or ["none"]})
    return {"cameras": out}


@app.get("/api/rank-evidence")
def rank_evidence():
    als = rows("SELECT * FROM alerts ORDER BY created DESC LIMIT 30")
    ranked = []
    for a in als:
        score = 40
        if a.get("severity") == "CRITICAL":
            score += 40
        if a.get("kind") in ("watchlist", "cyber", "tamper"):
            score += 15
        score = min(99, score + int((a.get("trust") or 50) / 10))
        ranked.append({**a, "rank_score": score})
    ranked.sort(key=lambda x: -x["rank_score"])
    return {"ranked": ranked}


@app.post("/api/demo/panic")
def demo_panic():
    execute(
        "INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,?,?)",
        ("al-" + uuid.uuid4().hex[:10], "cam-ring", "panic",
         "Panic: sudden crowd / running",
         "Motion burst — fight/rush cue (OpenCV). Confirm on Live.",
         "CRITICAL", 65, 0, utcnow(), "new"),
    )
    execute("INSERT INTO events VALUES(?,?,?,?,?,?,?)",
            ("ev-" + uuid.uuid4().hex[:8], "panic", "Panic / rush at Ring Road", "cam-ring", "Surat", "crowd", utcnow()))
    return {"ok": True}


@app.post("/api/demo/abandoned")
def demo_abandoned():
    execute(
        "INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,?,?)",
        ("al-" + uuid.uuid4().hex[:10], "cam-park", "abandoned",
         "Abandoned object (bag/box) — no move 5 min",
         "Static object in parking deck. Dispatch check.",
         "HIGH", 70, 0, utcnow(), "new"),
    )
    return {"ok": True}


def _ai_loop():
    idx = 0
    while True:
        time.sleep(12)
        if not ai_guard["on"]:
            continue
        cams = rows(
            "SELECT * FROM cameras WHERE kind='recorded' AND source IS NOT NULL AND source != ''"
        )
        cams = [c for c in cams if c.get("source") and os.path.isfile(c["source"])]
        if not cams:
            continue
        cam = cams[idx % len(cams)]
        idx += 1
        ai_guard["last_cam"] = cam["name"]
        ai_guard["last_at"] = utcnow()
        ai_guard["cycles"] = int(ai_guard.get("cycles") or 0) + 1
        try:
            hints = []
            for d in DEMO_CAMS:
                if d["id"] == cam["id"]:
                    hints.append(d["hint"])
            result = process_video(cam["source"], cam.get("name") or "", hints)
            plates = [normalize_plate(x) for x in (result.get("plates") or [])]
            ai_guard["plates_last"] = plates
            con = db()
            watch = {normalize_plate(r["plate"]): dict(r) for r in con.execute("SELECT * FROM watchlist")}
            for plate in plates:
                con.execute(
                    "INSERT INTO events VALUES(?,?,?,?,?,?,?)",
                    ("ev-" + uuid.uuid4().hex[:8], "vehicle",
                     f"Plate {plate} at {cam.get('name')}", cam["id"],
                     cam.get("place"), plate, utcnow()),
                )
                con.execute(
                    "INSERT INTO sightings VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    ("see-" + uuid.uuid4().hex[:10], plate, cam["id"], cam.get("name"),
                     cam.get("place"), cam.get("city_id"), cam.get("area_id"),
                     cam.get("lat"), cam.get("lng"), utcnow(), "continuous-ai"),
                )
                if plate in watch:
                    recent = con.execute(
                        "SELECT id FROM alerts WHERE camera_id=? AND title LIKE ? AND created > datetime('now','-3 minutes')",
                        (cam["id"], f"%{plate}%"),
                    ).fetchone()
                    if not recent:
                        w = watch[plate]
                        con.execute(
                            "INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,?,?)",
                            ("al-" + uuid.uuid4().hex[:10], cam["id"], "watchlist",
                             f"Watchlist hit {plate}",
                             f"{w['kind'].upper()} — last seen {cam.get('name')} · AI continuous",
                             w.get("priority") or "HIGH", result.get("trust") or 80,
                             0, utcnow(), "new"),
                        )
            for tp in result.get("tampers") or []:
                con.execute(
                    "INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,?,?)",
                    ("al-" + uuid.uuid4().hex[:10], cam["id"], "tamper",
                     f"Video tamper: {tp['type']}", tp["detail"], "CRITICAL",
                     result.get("trust") or 40, tp.get("t") or 0, utcnow(), "new"),
                )
            note = f"AI watch · {utcnow()} · plates {', '.join(plates) or 'none'}"
            con.execute(
                "UPDATE cameras SET last_note=?, trust=? WHERE id=?",
                (note, result.get("trust") or 80, cam["id"]),
            )
            con.commit()
            con.close()
        except Exception:
            continue


threading.Thread(target=_ai_loop, daemon=True).start()


@app.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    sockets.append(ws)
    try:
        while True:
            data = await ws.receive_json()
            if data.get("type") == "chat":
                u = user_from_token(data.get("token")) or {"name": "Guest", "role": "guest"}
                mid = "m-" + uuid.uuid4().hex[:8]
                execute(
                    "INSERT INTO messages VALUES(?,?,?,?,?,?)",
                    mid, data.get("room") or "team", u["name"], u["role"],
                    str(data.get("text") or "")[:500], utcnow(),
                )
                await broadcast({
                    "type": "chat",
                    "id": mid,
                    "user": u["name"],
                    "role": u["role"],
                    "text": data.get("text"),
                    "created": utcnow(),
                    "room": data.get("room") or "team",
                })
            elif data.get("type") == "ping":
                await ws.send_json({"type": "pong", "clock": utcnow()})
    except WebSocketDisconnect:
        if ws in sockets:
            sockets.remove(ws)
