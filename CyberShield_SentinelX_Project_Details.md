# CyberShield CCTV & Sentinel-X
## Detailed Project Brief, Architecture, Scope & Timeline

**Prepared:** 18 August 2026  
**Location context:** India (typical college / startup / MSME delivery)  
**Purpose:** Expand both project ideas into implementable products with honest effort estimates.

---

## How the two projects relate

| | **CyberShield CCTV** | **Sentinel-X** |
|---|---|---|
| **Role** | Security *of* the camera system | Security *through* the camera system |
| **Core question** | “Has anyone hacked, replayed, or edited this feed?” | “What threat is happening in the scene?” |
| **Primary AI** | Tamper / anomaly on the *signal* | Objects, faces, plates, weapons, deepfakes |
| **Best use** | Banks, courts, evidence rooms, police lockers | City CCTV, campuses, highways, malls |
| **Dependency** | Can stand alone | Stronger if it *includes* CyberShield integrity |

**Recommendation:** Treat CyberShield as **Phase-1 / foundation**. Build Sentinel-X on top as **Phase-2 platform**. Combined they match the workflow:

`Cameras → ingest (ONVIF/RTSP) → integrity + encryption → AI engine → threat + cyber alerts → React dashboard → police / SOC control room`

---

# PROJECT 1 — CyberShield CCTV

## 1. Problem

Traditional DVR/NVR systems fail in three ways:

1. **Video can be replaced** (looped old footage, black frames, frozen last-good-frame).
2. **Cameras can be hijacked** (default passwords, open RTSP, ONVIF without TLS).
3. **Evidence is not court-ready** (no hash chain, no chain-of-custody).

CyberShield protects the *pipeline*, not just the scene.

## 2. Objectives (measurable)

- Detect feed freeze / blackout / replay within **3 seconds**.
- SHA-256 (or HMAC-SHA-256) per GOP / N-second segment; mismatch → **TAMPERED**.
- Detect common camera attacks: brute-force ONVIF, RTSP scan, credential stuffing, ARP/DHCP spoofing on the CCTV VLAN (lab scope).
- Alert SOC + optional police control-room webhook in **< 5 seconds**.
- Store immutable audit log (append-only) with operator identity.

## 3. Modules (detailed)

### M1 — Camera monitoring & health
- Discover cameras (ONVIF WS-Discovery or manual IP list).
- Heartbeat: FPS, bitrate, resolution, packet loss, latency.
- Status: ONLINE / DEGRADED / OFFLINE / SUSPICIOUS.
- Stream ingest: OpenCV + FFmpeg (`rtsp://`), reconnect with exponential backoff.

### M2 — Video integrity verification
- **Segment hashing:** every 2–5 s of H.264/H.265 → SHA-256 → store `(camera_id, t_start, t_end, hash, prev_hash)`.
- **Hash chain:** each record includes previous hash (blockchain-lite, no public chain required).
- **Perceptual checks (OpenCV):**
  - Mean luminance → black-screen attack.
  - Frame-to-frame SSIM / MSE → freeze / replay loop.
  - Histogram shift → overlay / watermark wipe.
- **Optional forensic extras:** HMAC with camera-side key; AES-256 at rest for clips.

### M3 — Attack detection (cyber engine)
- Auth failure rate on camera / NVR APIs.
- Unexpected new MAC/IP on CCTV subnet (if you have a tap / pfSense log).
- Stream source IP change mid-session.
- Sudden codec / resolution change (injection).
- Simple IDS rules (Suricata or custom Python) for RTSP DESCRIBE floods.

### M4 — Alert generation
- Severity: INFO / WARN / CRITICAL.
- Channels: in-app, email, SMS (Twilio / MSG91), Telegram, webhook to police console.
- Dedup + cooldown so one freeze does not spam 200 alerts.
- Evidence pack: last 30 s clip + hash report + JSON incident.

### M5 — Dashboard (Flask API + React)
- Live camera grid with integrity badge (green / amber / red).
- Incident timeline, hash explorer (“verify this file”).
- Role-based access: Admin, Operator, Auditor, Police viewer.
- Reports: PDF daily integrity certificate.

### M6 — Data layer
- PostgreSQL: cameras, users, incidents, hash_chain, alerts.
- Object storage (MinIO / S3 / local disk) for clips.
- Redis: live status + pub/sub to React (Socket.IO).

## 4. Architecture

```
[IP Camera / NVR]
        | RTSP / ONVIF
        v
[Ingest Worker] --frames--> [Integrity Worker] --hashes--> PostgreSQL
        |                         |
        |                         +--> [Tamper Detector]
        v
[Cyber Sensor] --events--> [Alert Engine] --> [Flask REST + WS]
                                                    |
                                                    v
                                              [React Dashboard]
                                                    |
                                                    v
                                         [Police webhook / email]
```

**Suggested stack**
- Backend: Python 3.11, Flask or FastAPI, SQLAlchemy, Celery/RQ workers.
- Vision: OpenCV, NumPy, FFmpeg.
- Crypto: `hashlib.sha256`, `hmac`, `cryptography` (AES-GCM).
- Frontend: React 18, Vite, Tailwind, Recharts, Leaflet (optional map).
- DB: PostgreSQL 16 + Redis.
- Deploy: Docker Compose; optional NVIDIA only if you later add AI.

## 5. Workflow (as specified, expanded)

1. CCTV streams continuously into ingest.
2. **AI / CV analysis** scores freeze, blackout, scene cut, hash mismatch.
3. **Cybersecurity engine** correlates stream anomalies with network events.
4. Dashboard shows live trust score per camera.
5. Critical incidents push to police / control room with evidence hash.

## 6. What “done” looks like (MVP vs full)

| Feature | Student MVP | Production |
|---|---|---|
| Cameras | 2–4 RTSP (can be IP Webcam / files) | 50–500 ONVIF |
| Integrity | File + segment SHA-256 | Hardware TPM / camera HMAC |
| Attacks | Simulated (scripted) | Real VLAN + Suricata |
| Police room | Email / mock console | Secured VPN + audit |
| Auth | JWT + roles | SSO, 2FA, air-gapped auditor |

## 7. Timeline — CyberShield only

Assumes **2–3 people** (1 backend/CV, 1 frontend, 0.5 devops/docs), part-time college pace **~20–25 hrs/week each**, or full-time startup.

| Phase | Work | College team | Full-time (2–3 eng) |
|---|---|---|---|
| P0 Discovery | Threat model, camera inventory, schema | 1 week | 3–5 days |
| P1 Ingest + health | RTSP, camera CRUD, status | 2–3 weeks | 1.5 weeks |
| P2 Integrity | SHA-256 chain, verify UI | 2–3 weeks | 1.5 weeks |
| P3 Tamper CV | Freeze / black / loop | 2 weeks | 1 week |
| P4 Attack + alerts | Rules, notifications | 2 weeks | 1 week |
| P5 Dashboard polish | Grid, reports, RBAC | 2–3 weeks | 1.5 weeks |
| P6 Test + docs | Demo script, thesis report | 1–2 weeks | 1 week |
| **Total** | | **12–16 weeks (~3–4 months)** | **7–9 weeks** |

**Buffer for hardware pain (RTSP codecs, NAT, cheap cameras):** +2–3 weeks.

---

# PROJECT 2 — Sentinel-X

## 1. Problem

Cities and campuses have many cameras but **no unified brain**:
- Face watchlists, number plates, weapons, and deepfake/replay are separate products.
- Evidence is easy to leak or alter.
- Operators cannot see one threat picture.

Sentinel-X is a **unified AI + cyber surveillance platform**.

## 2. Objectives

- Ingest **multiple** ONVIF/RTSP cameras in one server.
- Real-time:
  - Face recognition (watchlist + stranger).
  - ANPR (Indian plates: KA, GJ, MH, etc.).
  - Weapon detection (pistol / rifle / knife — YOLOv8).
  - Deepfake / face-swap / injected synthetic video flags.
- Protect evidence with **AES-256** + hash chain (reuse CyberShield).
- Single React command dashboard + incident case file.

## 3. Modules (detailed)

### S1 — CCTV integration
- ONVIF: discover, PTZ (optional), profiles.
- RTSP pull with per-camera worker pool.
- Adaptive downscale (e.g. detect at 640–1280 px, archive full HD).
- Camera groups: Gate, Parking, Lobby, Perimeter.

### S2 — Face recognition
- Detect: YOLO-face or InsightFace / SCRFD.
- Embed: ArcFace (InsightFace).
- Gallery in PostgreSQL + FAISS / pgvector.
- Liveness (blink / texture) to reduce photo-on-phone spoof (basic).
- Privacy: blur non-watchlist faces in public views (policy flag).

### S3 — ANPR
- Detect plate (YOLOv8 custom).
- OCR: PaddleOCR or EasyOCR, tuned for Indian fonts.
- Rules: stolen list, banned vehicle, VIP whitelist, parking time.

### S4 — Weapon / threat detection
- YOLOv8n/s trained or fine-tuned on weapon + person + bag.
- Track with ByteTrack (same weapon across frames → one incident).
- Confidence threshold + human confirm button (reduce false positives).

### S5 — Deepfake / injection detection
- **Signal level (from CyberShield):** hash, freeze, codec jump.
- **Face level:** frequency artifacts, blink rate, identity flicker, MesoNet / simple CNN.
- Honest scope: **lab-grade detector**, not Hollywood-proof. Document false-positive rate.

### S6 — Evidence protection
- AES-256-GCM on stored clips; keys in env / Vault.
- SHA-256 chain + export “court pack” (video + hashes + operator log).
- Watermark overlay: camera ID + UTC timestamp (visible) + invisible hash note.

### S7 — Threat analysis & fusion
- Correlate: “unknown face + weapon near gate” → CRITICAL.
- Time window + geofence (camera location).
- Priority queue for operators.

### S8 — Dashboard
- Multi-camera mosaic, bounding boxes via WebRTC or MJPEG/HLS.
- Watchlists (faces, plates).
- Incident board (Kanban: New / Acknowledged / Dispatched / Closed).
- Map of cameras (Surat / campus GeoJSON).
- Police control-room role: read-only live + download evidence.

## 4. Architecture

```
 Camera farm (ONVIF/RTSP)
           |
    [Integration Server]
     |              |
  [Hash/AES]    [GPU Inference]
     |           YOLO | Face | ANPR | DF
     |              |
     +----->[Fusion / Threat bus]
                   |
         Flask/FastAPI + Redis
                   |
         React Command Center
                   |
         Police / SOC adapters
```

**Stack**
- AI: Ultralytics YOLOv8, PyTorch, InsightFace, PaddleOCR, OpenCV.
- Video: FFmpeg, optional NVIDIA Video Codec SDK.
- API: FastAPI (better than Flask for async streams) — Flask still OK for academic spec.
- Front: React, HLS.js / WebRTC.
- DB: PostgreSQL + pgvector or FAISS, MinIO, Redis.
- Hardware (realistic):
  - Demo: 1× RTX 3060/4060, 4–8 streams at 10–15 FPS detect.
  - Site: 1 GPU per ~8–16 AI streams (YOLOv8s).

## 5. Workflow

`Multiple cameras → integration server → AI engine (parallel models) → threat analysis (fusion) → dashboard → human / police action`

## 6. Timeline — Sentinel-X

This is **significantly larger**. Dataset collection and false-positive tuning dominate.

| Phase | Work | College (3–4 people) | Full-time (4–5 eng + 1 ML) |
|---|---|---|---|
| P0 | Architecture, datasets, legal/privacy note | 2 weeks | 1 week |
| P1 | Multi-camera ingest + dashboard shell | 3 weeks | 2 weeks |
| P2 | YOLOv8 person/weapon + tracking | 3–4 weeks | 2 weeks |
| P3 | Face gallery + recognition | 3–4 weeks | 2–3 weeks |
| P4 | ANPR (Indian plates) | 3 weeks | 2 weeks |
| P5 | Deepfake / tamper (basic) | 2–3 weeks | 2 weeks |
| P6 | AES + evidence pack + fusion rules | 2–3 weeks | 1.5 weeks |
| P7 | Control room UX, alerts, load test | 3 weeks | 2 weeks |
| P8 | Field pilot (4–8 real cameras) | 2–4 weeks | 2 weeks |
| **Total** | | **6–8 months** | **14–18 weeks (~4 months)** |

If you **reuse CyberShield** as the ingest/integrity layer, subtract **4–6 weeks** from Sentinel-X.

## 7. Combined program (recommended)

| Milestone | Deliverable | Cumulative time (college) | Full-time |
|---|---|---|---|
| M1 | CyberShield MVP (4 cams, hash, tamper, alerts) | Month 3–4 | Week 8 |
| M2 | + YOLO threats + dashboard mosaic | Month 5–6 | Week 12 |
| M3 | + Face + ANPR | Month 7–8 | Week 16 |
| M4 | + Deepfake flag + police console + AES evidence | Month 8–10 | Week 18–20 |

**Headline numbers**
- **CyberShield alone:** 3–4 months (students) / **2 months** (full-time).
- **Sentinel-X alone:** 6–8 months (students) / **4 months** (full-time).
- **Both as one product (Sentinel-X with CyberShield inside):** **8–10 months** students / **4.5–5 months** full-time.

A **final-year B.Tech project** should **narrow Sentinel-X**: pick **2 AI modules** (e.g. weapon + integrity, or ANPR + face) plus dashboard. Full six-module Sentinel-X is a **startup MVP**, not a single-semester solo project.

---

# Team, cost, risks

## Suggested team

| Role | CyberShield | Sentinel-X |
|---|---|---|
| Backend / Python | 1 | 1 |
| CV / ML | 0.5 | 1–2 |
| React | 1 | 1 |
| DevOps / GPU | 0.2 | 0.5 |
| Domain (police/security advisor) | optional | strongly useful |

## Indicative cost (India, 2026, excluding salaries)

| Item | Student lab | Small deployment |
|---|---|---|
| GPUs | Colab / 1 used RTX | 1–2× RTX 4070/L4 |
| Cameras | 0 (use phone RTSP) | ₹8k–40k each IP cam |
| Server | existing PC | ₹1.5–4 L |
| SMS/cloud | ₹0–2k | ₹5–20k/mo |
| Domain + VPS | ₹5–15k/yr | more |

## Major risks (plan for them)

1. **False positives** on weapons (phones, umbrellas) — always require human confirm.
2. **RTSP instability** on cheap cameras — invest time in FFmpeg reconnect.
3. **Face recognition law / DPDP Act (India)** — consent, purpose limitation, retention policy. Write this in the report.
4. **Deepfake SOTA moves fast** — treat as *indicator*, not proof.
5. **GPU cost** — use YOLOv8n + every Nth frame.
6. **Court evidence** — hash chain helps; get a lawyer note if you claim legal admissibility.

## Academic / demo scope (safe and impressive)

**CyberShield demo (15 min)**
1. Play live webcam.
2. Pause / loop file → TAMPER alert + hash mismatch.
3. Download evidence PDF with SHA-256.

**Sentinel-X demo (15 min)**
1. Four video files as “cameras”.
2. Weapon clip → box + CRITICAL.
3. Plate image → ANPR hit.
4. Enrolled teammate face → match.
5. Show AES-locked clip + unlock with role.

---

# Suggested repository layout

```
cybershield/          or sentinelx/
  backend/
    app/              # Flask/FastAPI
    workers/          # ingest, hash, infer
    models/           # yolov8*.pt
  frontend/           # React
  docker-compose.yml
  docs/threat-model.md
  datasets/README.md  # do not commit raw faces
```

---

# What to write in a synopsis (copy-ready)

**CyberShield CCTV** is a cybersecurity layer for existing CCTV. It continuously monitors camera health, computes SHA-256 hash chains on video segments, detects tampering (freeze, blackout, replay) with OpenCV, flags network/stream attacks, and pushes alerts to a Flask–React dashboard and a police control-room channel. PostgreSQL stores the immutable audit trail.

**Sentinel-X** is a unified surveillance platform that connects many ONVIF/RTSP cameras, runs YOLOv8-based weapon detection, face recognition, ANPR, and basic deepfake/injection checks, encrypts evidence with AES, and fuses events into one operator dashboard. It is designed so CyberShield integrity sits under the AI engine.

---

# Decision guide

- **Only 1 semester, 2 students:** CyberShield only.
- **Final year, 4 students, GPU available:** CyberShield + weapon + one of {face, ANPR}.
- **Startup / funded 5-month build:** Full Sentinel-X including CyberShield.
- **Need a police pilot:** Add 4 extra weeks for SOPs, false-alarm tuning, and air-gapped export.

If you want, next step can be a **week-by-week Gantt**, **database ER diagram**, or a **starter repo** (Flask + React + hash worker + dummy YOLO).
