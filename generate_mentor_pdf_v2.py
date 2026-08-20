#!/usr/bin/env python3
"""Full mentor briefing aligned to Gujarat Police Innovation Challenge 2026 portal steps."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether,
)
from reportlab.lib.enums import TA_JUSTIFY

OUT = "/home/user/SentinelShield_Mentor_Briefing.pdf"

NAVY = HexColor("#0B1F3A")
TEAL = HexColor("#0D7377")
PURPLE = HexColor("#5B21B6")
SLATE = HexColor("#334155")
LIGHT = HexColor("#F1F5F9")
SOFT = HexColor("#E2E8F0")
AMBER = HexColor("#B45309")
GREEN = HexColor("#166534")

PAGE_W, PAGE_H = A4


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 15 * mm, PAGE_W, 15 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H - 16.2 * mm, PAGE_W, 1.2 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Times-Bold", 8.5)
    canvas.drawString(16 * mm, PAGE_H - 9.5 * mm, "SentinelShield  |  Mentor Briefing for Gujarat Police Innovation Challenge 2026")
    canvas.setFont("Times-Roman", 8)
    canvas.drawRightString(PAGE_W - 16 * mm, PAGE_H - 9.5 * mm, "Academic / Hackathon")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, 11 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, 11 * mm, PAGE_W, 0.7 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(16 * mm, 4.5 * mm, "Maps official portal Steps 1–7  ·  sentinel.gujarat.gov.in  ·  ₹0 student prototype")
    canvas.drawRightString(PAGE_W - 16 * mm, 4.5 * mm, f"Page {doc.page}")
    canvas.restoreState()


def styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(name="Kicker", fontName="Times-Bold", fontSize=9,
                         textColor=TEAL, alignment=TA_CENTER, spaceAfter=4))
    s.add(ParagraphStyle(name="CoverTitle", fontName="Times-Bold", fontSize=22,
                         textColor=NAVY, alignment=TA_CENTER, leading=26, spaceAfter=6))
    s.add(ParagraphStyle(name="CoverSub", fontName="Times-Italic", fontSize=11,
                         textColor=SLATE, alignment=TA_CENTER, leading=15, spaceAfter=3))
    s.add(ParagraphStyle(name="H1", fontName="Times-Bold", fontSize=13,
                         textColor=NAVY, spaceBefore=10, spaceAfter=5, leading=16))
    s.add(ParagraphStyle(name="H2", fontName="Times-Bold", fontSize=11,
                         textColor=TEAL, spaceBefore=7, spaceAfter=3, leading=14))
    s.add(ParagraphStyle(name="H3", fontName="Times-Bold", fontSize=10,
                         textColor=PURPLE, spaceBefore=5, spaceAfter=2, leading=13))
    s.add(ParagraphStyle(name="Body", fontName="Times-Roman", fontSize=9.5,
                         textColor=SLATE, alignment=TA_JUSTIFY, leading=13, spaceAfter=5))
    s.add(ParagraphStyle(name="BulletBody", fontName="Times-Roman", fontSize=9.5,
                         textColor=SLATE, leading=12.5))
    s.add(ParagraphStyle(name="Cell", fontName="Times-Roman", fontSize=8,
                         textColor=SLATE, leading=10.8))
    s.add(ParagraphStyle(name="CellH", fontName="Times-Bold", fontSize=8,
                         textColor=white, leading=10.8))
    s.add(ParagraphStyle(name="Caption", fontName="Times-Italic", fontSize=8,
                         textColor=SLATE, alignment=TA_CENTER, spaceBefore=1, spaceAfter=7))
    s.add(ParagraphStyle(name="Note", fontName="Times-Italic", fontSize=8.5,
                         textColor=SLATE, leading=11.5, spaceAfter=5))
    s.add(ParagraphStyle(name="FooterNote", fontName="Times-Roman", fontSize=8,
                         textColor=SLATE, alignment=TA_CENTER, leading=11))
    return s


def P(text, style):
    return Paragraph(text, style)


def table(data, col_widths, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY) if header else ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white) if header else ("TEXTCOLOR", (0, 0), (-1, 0), NAVY),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Times-Roman"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (0, 1), (-1, -1), SLATE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("GRID", (0, 0), (-1, -1), 0.25, SOFT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
    ]
    t.setStyle(TableStyle(cmds))
    return t


def bullets(items, st):
    out = []
    for it in items:
        out.append(P("•  " + it, st["BulletBody"]))
    out.append(Spacer(1, 3))
    return out


def build():
    st = styles()
    C, H = st["Cell"], st["CellH"]
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=15 * mm, rightMargin=15 * mm,
        topMargin=20 * mm, bottomMargin=16 * mm,
        title="SentinelShield — Mentor Briefing (GPIC 2026)",
        author="Project Team",
        subject="Full mapping to Gujarat Police Innovation Challenge 2026 official steps",
    )
    story = []

    # ========== COVER ==========
    story.append(Spacer(1, 4 * mm))
    story.append(P("PROJECT BRIEFING FOR FACULTY MENTOR  ·  18 AUGUST 2026", st["Kicker"]))
    story.append(P("SentinelShield", st["CoverTitle"]))
    story.append(P("Integrity-aware statewide CCTV integration and AI watchlist platform", st["CoverSub"]))
    story.append(P(
        "Prepared for <b>Gujarat Police Innovation Challenge 2026</b> "
        "(portal: sentinel.gujarat.gov.in)  ·  Category: Students / MSME startups",
        st["CoverSub"],
    ))
    story.append(Spacer(1, 3 * mm))

    meta = [
        [P("<b>Official event</b>", C),
         P("Gujarat Police Innovation Challenge 2026 — CCTV integration + AI analytics; prize pool reported ₹37 lakh; finale = live production feeds; partners i-Hub, DA-IICT, NFSU.", C)],
        [P("<b>Our product name</b>", C),
         P("SentinelShield = CyberShield CCTV (integrity / cyber) + Sentinel-X (AI / watchlist / GIS).", C)],
        [P("<b>Chosen official model</b>", C),
         P("<b>Hybrid:</b> Model 1 Registry &amp; GIS (MANDATORY) + Model 3 VMS Federation/Middleware + Model 2 Unified Viewing &amp; Analytics. Not a rip-and-replace Central VMS (Model 4).", C)],
        [P("<b>Budget + time (one state)</b>", C),
         P("Gujarat full implementation: <b>₹38.4 Cr total</b> (₹32 Cr build + ₹6.4 Cr hypercare) over <b>36 months to statewide go-live</b>, then 12 months stabilise (48 months programme). Student prototype still <b>₹0 / 5 weeks</b>. Detail §8.7–8.8.", C)],
        [P("<b>Decision asked</b>", C),
         P("Approve this as the official college project / hackathon entry and the scope in Section 16.", C)],
    ]
    mt = Table(meta, colWidths=[38 * mm, 142 * mm])
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.7, TEAL),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(mt)

    story.append(P("1.  Why this document exists", st["H1"]))
    story.append(P(
        "The official hackathon portal is organised as seven steps (Understand → Models → Solution approach → "
        "50-camera live test → Submit → Scale to ~80,000 cameras → Evaluation). Our earlier CyberShield / "
        "Sentinel-X notes did <b>not</b> cover GIS, camera registry, VMS federation, 50-camera onboarding, "
        "watchlist matching, vehicle route history, department-wise data, cost–benefit, or statewide rollout. "
        "This briefing <b>fills every official box</b> so the mentor can see that the project is aligned to "
        "Gujarat Police’s problem — not only a college YOLO demo.",
        st["Body"],
    ))

    # ========== STEP 1 ==========
    story.append(P("2.  STEP 1 — Understand the challenge (official)", st["H1"]))
    story.append(P(
        "Gujarat Police want one usable picture from more than <b>80,000 CCTV cameras</b> that today sit on "
        "different departments, vendors, Video Management Systems (VMS), codecs and networks. "
        "The challenge is not “train one more detector”. It is <b>integration + trust + analytics + scale</b>.",
        st["Body"],
    ))
    story.append(P("2.1  Four key challenges from the portal — and our response", st["H2"]))
    ch = [
        [P("Official key challenge", H), P("What it means in Gujarat", H), P("What SentinelShield does", H)],
        [P("Heterogeneous infrastructure", C),
         P("Safe City, traffic, municipal, campus, highway, police thana cameras; ONVIF / proprietary / NVR-only; H.264/H.265; different time sync.", C),
         P("Adapter layer per source type (RTSP, ONVIF, VMS export, file, HLS). Camera registry stores vendor, codec, timezone, owner dept.", C)],
        [P("Multiple VMS &amp; vendors", C),
         P("Milestone, Genetec, HikCentral, CP Plus, iVMS, custom NVRs cannot be replaced overnight.", C),
         P("<b>Federation, not rip-and-replace.</b> We pull streams or events via RTSP/ONVIF/API; existing VMS stays for recording.", C)],
        [P("Network, security &amp; interoperability", C),
         P("Open RTSP, default passwords, no TLS, spoofed / looped video, no common ID for a camera.", C),
         P("CyberShield: SHA-256 hash chain, freeze/black/replay detect, RBAC, AES evidence, camera identity in registry.", C)],
        [P("Analytics &amp; scalability to ~80,000 cameras", C),
         P("Cannot run GPU on every stream 24×7. Need watchlist + ANPR + search, not wall-of-screens.", C),
         P("Tiered AI: metadata-only on most cams; full infer on hotlist / event / sampled streams. Horizontal GPU workers.", C)],
    ]
    story.append(table(ch, [42 * mm, 69 * mm, 69 * mm]))
    story.append(P("Table 1. Portal Step 1 mapped to the project.", st["Caption"]))

    story.append(P("2.2  Statewide vision we accept", st["H2"]))
    story.extend(bullets([
        "One <b>camera registry</b> and map (GIS) for every on-boarded camera in Gujarat.",
        "Police can search a plate / person / incident across districts without logging into 20 VMS consoles.",
        "Live alerts when a watchlist entity appears; officer can replay a trusted clip with a hash.",
        "Departments keep ownership of cameras; Police get a lawful, role-based view.",
        "Human-in-the-loop: AI proposes, officer confirms (reduces false dispatch).",
    ], st))

    # ========== STEP 2 ==========
    story.append(P("3.  STEP 2 — Integration model we choose", st["H1"]))
    story.append(P(
        "The portal lists four reference models plus Hybrid. <b>Model 1 is mandatory.</b> "
        "We do not pick Model 4 as the only path: forcing every district onto one new VMS is politically "
        "and operationally unrealistic in a 80k mixed estate.",
        st["Body"],
    ))
    models = [
        [P("Portal model", H), P("Our stance", H), P("How it appears in SentinelShield", H)],
        [P("1. Registry &amp; GIS Foundation  [MANDATORY]", C),
         P("<b>Must build</b>", C),
         P("camera_id, lat/long, district, PS, dept, vendor, VMS, stream URL (vaulted), health, last hash. Leaflet / OpenStreetMap map + GeoJSON.", C)],
        [P("2. Unified Viewing &amp; Analytics", C),
         P("Build for PoC + scale design", C),
         P("React mosaic of selected cameras; AI overlays; alert inbox; not a 80k live wall.", C)],
        [P("3. VMS Federation &amp; Middleware", C),
         P("<b>Primary integration strategy</b>", C),
         P("Ingest adapters + message bus. Existing NVRs keep archive. We federate live + metadata.", C)],
        [P("4. Central VMS &amp; AI Platform", C),
         P("Not our v1; optional long-term", C),
         P("Would mean replacing district VMS. We document as Phase-3 only.", C)],
        [P("Hybrid / Innovative", C),
         P("<b>Official choice on the form</b>", C),
         P("1 + 3 + 2, plus CyberShield integrity as the innovative layer judges usually miss.", C)],
    ]
    story.append(table(models, [52 * mm, 38 * mm, 90 * mm]))
    story.append(P("Table 2. Step 2 — tick Hybrid; implement Model 1 as the backbone.", st["Caption"]))

    story.append(P(
        "<b>Innovation claim for mentors/judges:</b> federation platforms show video; they rarely prove the "
        "frame was not looped. SentinelShield attaches a <b>trust score</b> to every camera and every alert. "
        "A stolen-car hit on a tampered feed is marked UNTRUSTED.",
        st["Body"],
    ))

    # ========== STEP 3 ==========
    story.append(P("4.  STEP 3 — Expected solution approach (all ten official tiles)", st["H1"]))
    story.append(P(
        "Portal text: build a deployment-ready design that continuously processes provided CCTV feeds; "
        "integrate live streams with a <b>searchable watchlist</b> (stolen vehicles, wanted / missing persons, "
        "blacklisted vehicles, suspect lists); continuous AI; automated alerts on match; full workflow "
        "(database, matching, alerting, UI); representative datasets; evaluators may ask us to find a "
        "specified vehicle or entity in the feeds in real time.",
        st["Body"],
    ))

    story.append(P("4.1  Overall architecture", st["H2"]))
    story.append(P(
        "Logical layers: (1) Edge / existing VMS, (2) Adapter &amp; ingest, (3) Registry &amp; GIS, "
        "(4) Integrity engine, (5) AI workers (ANPR, vehicle, person/face-optional, activity), "
        "(6) Watchlist matcher, (7) Fusion &amp; case file, (8) API, (9) Operator console + GIS, "
        "(10) Audit / evidence store.",
        st["Body"],
    ))
    story.append(P(
        "<font face='Courier' size='8'>Dept cameras / VMS → Adapters (RTSP/ONVIF/API) → Ingest bus → "
        "Registry+GIS | Hash-chain | AI workers → Watchlist match → Fusion → API → React+Map → Officer</font>",
        st["Note"],
    ))

    story.append(P("4.2  Integration strategy", st["H2"]))
    story.extend(bullets([
        "<b>Do not rip VMS.</b> Onboard via: ONVIF device service, RTSP URL from NVR, vendor API if given, or secure file/HLS drop for air-gapped sites.",
        "Each camera gets a UUID in the registry before the first frame is accepted (Model 1 first).",
        "Time: NTP policy; store both camera timestamp and server UTC (fixes vendor clock drift).",
        "Multi-tenant: owner department vs Police viewer vs State SOC, via roles.",
        "For the 50-camera test: CSV/Excel bulk onboard (IP, RTSP, lat, long, PS name) + health ping.",
        "Government-feed day: same adapters; credentials injected by organisers, never hard-coded.",
    ], st))

    story.append(P("4.3  AI and video analytics", st["H2"]))
    ai = [
        [P("Analytic", H), P("Hackathon / PoC", H), P("Why Police need it", H)],
        [P("Vehicle detect + track", C), P("YOLOv8 + ByteTrack", C), P("Follow a car across frames and cameras", C)],
        [P("ANPR (Indian plates)", C), P("Plate YOLO + PaddleOCR / EasyOCR; GJ, MH, RJ… patterns", C), P("Stolen / blacklisted / suspect vehicle", C)],
        [P("Watchlist person", C), P("Optional InsightFace on consented / synthetic gallery only", C), P("Wanted / missing — high ethics bar", C)],
        [P("Tamper / freeze / loop", C), P("OpenCV + SHA-256 chain", C), P("Do not chase a ghost on looped video", C)],
        [P("Cross-camera search", C), P("Plate / track-id / time-window query", C), P("Route reconstruction", C)],
        [P("Unusual activity (v2)", C), P("Out of PoC unless time", C), P("Crowd / loiter — document as roadmap", C)],
    ]
    story.append(table(ai, [42 * mm, 78 * mm, 60 * mm]))
    story.append(P("Table 3. Analytics stack. Evaluation will likely force a designated vehicle.", st["Caption"]))
    story.append(P(
        "Matching logic: normalise plate (strip spaces, map O/0); fuzzy Levenshtein ≤ 1 for OCR noise; "
        "watchlist tables with list_type, valid_from/to, issuing_unit, priority. Hit = event + clip + GIS pin. "
        "Officer Confirm / Reject. Reject feeds active learning later.",
        st["Body"],
    ))

    story.append(P("4.4  Cybersecurity architecture (was missing in first notes)", st["H2"]))
    story.extend(bullets([
        "Identity: JWT + roles (Admin, Onboarder, Operator, Auditor, Police-view). 2FA in scale design.",
        "Stream secrets in vault / env, never in Git. TLS on API. Separate CCTV VLAN in scale design.",
        "Integrity: SHA-256 per 2–5 s segment + previous-hash chain; verify UI for any exported file.",
        "Tamper sensors: black, freeze, replay, sudden resolution/codec change, source-IP change.",
        "Evidence: AES-256-GCM export; audit log append-only (who watched, who exported).",
        "Privacy: DPDP Act 2023 — purpose limitation, retention, no public GitHub of real faces/plates from gov feeds.",
        "Hardening: no default passwords doc for field cams; ONVIF digest; disable UPnP in rollout SOP.",
    ], st))

    story.append(P("4.5  Deployment architecture", st["H2"]))
    story.extend(bullets([
        "<b>PoC / own-feed:</b> Docker Compose on one laptop or college PC (API, worker, DB, React, optional Redis).",
        "<b>50-camera live test:</b> 1× GPU box (or organiser GPU) + 1× CPU API + Postgres + object store; workers autoscale by queue depth.",
        "<b>District:</b> ingest close to bandwidth (district DC or police line); only metadata + alerts to State SOC.",
        "<b>State:</b> registry, watchlists, GIS, case search, policy. Edge does pixels; centre does decisions.",
        "Kubernetes later; Docker is enough to score “deployment-ready” if compose files + env samples exist.",
    ], st))

    story.append(P("4.6  Infrastructure sizing (indicative — for mentor, not a purchase indent)", st["H2"]))
    size = [
        [P("Tier", H), P("Cameras", H), P("What we run", H), P("Rough compute", H)],
        [P("Student prototype", C), P("3–8 virtual + phone", C), P("YOLOv8n every 3rd frame, CPU", C), P("1 laptop, ₹0", C)],
        [P("Live test (Step 4)", C), P("~50 heterogeneous", C), P("ANPR+track on all or on motion; 10–15 FPS detect", C),
         P("1× RTX 4090 / L4 class or 2× 3060; 32–64 GB RAM; 10 GbE if local", C)],
        [P("District (design)", C), P("2,000–8,000", C), P("Hotlist streams + sampled rest", C),
         P("GPU farm sized on <i>policy</i>, not 1 GPU/camera", C)],
        [P("State (design)", C), P("~80,000", C), P("Metadata plane + search + GIS", C),
         P("See Section 8; phased, not day-1 full infer", C)],
    ]
    story.append(table(size, [36 * mm, 38 * mm, 58 * mm, 48 * mm]))
    story.append(P("Table 4. Sizing philosophy: never promise 80k simultaneous full-HD YOLO.", st["Caption"]))

    story.append(P("4.7  Cost–benefit analysis (student honesty + police value)", st["H2"]))
    story.append(P(
        "Student build cost is ₹0. Statewide TCO is a design estimate for judges, not our invoice. "
        "Benefit is officer-hours saved on manual rewind, faster stolen-vehicle recovery, and fewer "
        "false pursuits on tampered video.",
        st["Body"],
    ))
    cba = [
        [P("Item", H), P("Without platform (today)", H), P("With SentinelShield (target)", H)],
        [P("Find one vehicle across cities", C), P("Hours–days;  many VMS logins; CD transport", C),
         P("Seconds–minutes; plate search + GIS path", C)],
        [P("Trust in clip for investigation", C), P("Often none; easy loop attack", C),
         P("Hash chain + tamper flag; NFSU-friendly pack", C)],
        [P("New VMS licence for 80k", C), P("Very high if Model 4 forced", C),
         P("Reuse existing VMS; pay for middleware + GPU only", C)],
        [P("Student / college cash", C), P("—", C), P("₹0 prototype; optional ₹15k cams after win", C)],
        [P("Indicative state software+GPU (design only)", C), P("Fragmented spend + risk of ₹200–400 Cr VMS rip-out", C),
         P("See §8.7: PoC ₹22 L · pilot ₹1.6 Cr · 4-yr state ₹32 Cr · ≈ ₹4,000 / camera", C)],
    ]
    story.append(table(cba, [48 * mm, 66 * mm, 66 * mm]))
    story.append(P("Table 5. Cost–benefit narrative for Step 3 tile and Step 6.", st["Caption"]))

    story.append(P("4.8  Department-wise information requirements", st["H2"]))
    dept = [
        [P("Department / unit", H), P("What they own / give us", H), P("What they consume", H)],
        [P("Gujarat Police (CID / Control / Traffic)", C),
         P("Watchlists, FIR-linked plates, live test credentials, SOP for confirm/reject", C),
         P("Alerts, GIS tracks, evidence pack, audit", C)],
        [P("Home / Safe City / Smart City SPVs", C),
         P("Camera inventory, GIS coordinates, VMS access", C), P("Health of their estate, shared incidents", C)],
        [P("RTO / Transport", C), P("Stolen / blacklisted vehicle feeds (API or file)", C), P("Match confirmations", C)],
        [P("Municipal corp. / ULBs", C), P("Ward cameras, junctions", C), P("Limited role; not crime dossiers", C)],
        [P("Highways / R&amp;B / GSRDC", C), P("Highway CCTV, chainage + GIS", C), P("Vehicle route on corridor", C)],
        [P("Campus / jail / court complexes", C), P("Closed networks; maybe file drop only", C), P("Local SOC view", C)],
        [P("Forensics (NFSU partner)", C), P("Hash / chain-of-custody guidance", C), P("Export standard", C)],
        [P("i-Hub / mentor college", C), P("GPU hours, ethics review", C), P("Publication / PoC", C)],
    ]
    story.append(table(dept, [52 * mm, 64 * mm, 64 * mm]))
    story.append(P("Table 6. Step 3 — department-wise information. Watchlists never sit in the student Git repo.", st["Caption"]))

    story.append(P("4.9  Scalability strategy (preview; detail in Step 6)", st["H2"]))
    story.extend(bullets([
        "Scale metadata and registry first (cheap), pixels second (expensive).",
        "AI only on: watchlist-proximate cameras, motion, junction samples, officer-requested rewind.",
        "Shard ingest by district; one logical watchlist (replicated).",
        "Object storage lifecycle: hot 7–30 days clips for alerts; hashes kept years; raw video stays on existing NVR.",
    ], st))

    story.append(P("4.10  Future roadmap", st["H2"]))
    story.extend(bullets([
        "P0 Prototype (now): registry+GIS mock, 4–8 feeds, hash, ANPR, alerts, UI.",
        "P1 50-cam live test: bulk onboard, designated vehicle, route history.",
        "P2 District pilot: one city / one zone, real SOP, 2FA, DR drill.",
        "P3 Multi-district; optional face if legal cell approves; activity analytics.",
        "P4 Statewide registry complete; Model 4 only if Home Dept. mandates a single VMS later.",
    ], st))

    # ========== DATA MODEL ==========
    story.append(P("5.  Data model (watchlist + matching — evaluators will look here)", st["H1"]))
    dm = [
        [P("Table", H), P("Key fields", H)],
        [P("cameras", C), P("id, name, district, police_station, dept, vendor, vms, lat, lon, status, trust_score, onboarded_at", C)],
        [P("streams", C), P("camera_id, protocol, endpoint_ref, codec, fps, last_frame_utc", C)],
        [P("hash_chain", C), P("camera_id, t_start, t_end, sha256, prev_sha256, ok", C)],
        [P("watchlist_vehicle", C), P("plate_norm, list_type (stolen/black/suspect), case_ref, priority, valid_to, issuing_unit", C)],
        [P("watchlist_person", C), P("temp_id, list_type (wanted/missing), embedding_ref, legal_basis, valid_to", C)],
        [P("detections", C), P("camera_id, ts, class, plate_ocr, track_id, conf, bbox, clip_uri", C)],
        [P("matches", C), P("detection_id, watchlist_id, score, status (new/ack/confirmed/false)", C)],
        [P("tracks", C), P("entity_key, points[] (cam, ts, lat, lon), route_geojson", C)],
        [P("alerts", C), P("severity, type, camera_id, match_id, trust, notified_roles", C)],
        [P("audit", C), P("who, action, object, ts, ip — append-only", C)],
    ]
    story.append(table(dm, [42 * mm, 138 * mm]))
    story.append(P("Table 7. Minimum schema so “searchable database of watchlist records” is real.", st["Caption"]))

    # ========== STEP 4 ==========
    story.append(P("6.  STEP 4 — Technical evaluation / live test case (~50 cameras)", st["H1"]))
    story.append(P(
        "Portal live challenge: onboard ~50 heterogeneous cameras, integrate live feeds, track a designated "
        "vehicle, generate alerts and history, visualise on GIS, show route / movement history and searchable events.",
        st["Body"],
    ))
    live = [
        [P("Official tile", H), P("How we will pass it", H), P("Demo script", H)],
        [P("Onboard ~50 cameras", C),
         P("CSV import → registry. Mix: RTSP, file-loop “broken vendor”, HTTP phone, missing-GPS row (shows validation).", C),
         P("Import 50 rows in &lt; 2 min; 48 green, 2 red with reason.", C)],
        [P("Integrate live feeds", C),
         P("Workers subscribe; mosaic shows 6–12 live, rest as health dots on map (cannot show 50 HD tiles).", C),
         P("Open 4 live + map of 50 heartbeats.", C)],
        [P("Track vehicle", C),
         P("ANPR + track_id; if plate unreadable, manual lock on bbox.", C),
         P("Organiser plate X → first hit in seconds.", C)],
        [P("Alerts &amp; history", C),
         P("Watchlist hit → CRITICAL; operator ack; timeline of all hits.", C),
         P("Show inbox + filter by plate/date.", C)],
        [P("Visualise on GIS", C),
         P("OpenStreetMap / Leaflet; camera markers; hit pulses; district boundary GeoJSON (Gujarat).", C),
         P("Zoom Ahmedabad / Surat / highway as data allows.", C)],
        [P("Route, movement, search", C),
         P("Polyline of hit cameras in time order; table of searchable events (plate, cam, ts, trust).", C),
         P("Play “vehicle went Cam12 → Cam7 → Cam41”.", C)],
    ]
    story.append(table(live, [40 * mm, 78 * mm, 62 * mm]))
    story.append(P("Table 8. Step 4 acceptance tests we will rehearse before the live window.", st["Caption"]))
    story.append(P(
        "If organisers give only a subset of 50 as truly live, we still onboard 50 records (registry completeness) "
        "and mark offline cameras honestly — that is better than fake green badges.",
        st["Body"],
    ))

    # ========== STEP 5 ==========
    story.append(P("7.  STEP 5 — Prepare and submit (official deliverables)", st["H1"]))
    sub = [
        [P("Portal deliverable", H), P("Our artefact", H), P("Owner", H)],
        [P("Solution presentation", C), P("12–15 slides: problem, hybrid model, architecture, live test, scale, ethics, ₹0 PoC", C), P("Pitch lead", C)],
        [P("High-Level Design document", C), P("This PDF expanded + diagrams (C4 context, sequence for match, ER)", C), P("Architect", C)],
        [P("Own-feed demonstration", C), P("Laptop demo: files + phone RTSP + tamper button + watchlist plate we filmed", C), P("ML + UI", C)],
        [P("Government-feed demonstration", C), P("Same binary; env file for official RTSP; no code change", C), P("Backend", C)],
        [P("Video &amp; output report", C), P("5–8 min unlisted video + 8–10 page output (metrics, screenshots, limitations)", C), P("All", C)],
        [P("Submission links", C), P("GitHub (private if required), demo URL / recording, drive of HLD + PPT", C), P("TL", C)],
    ]
    story.append(table(sub, [48 * mm, 100 * mm, 32 * mm]))
    story.append(P("Table 9. Nothing on the portal submit page is left blank.", st["Caption"]))

    # ========== STEP 6 ==========
    story.append(P("8.  STEP 6 — Plan for scale (~80,000 cameras across Gujarat)", st["H1"]))
    story.append(P(
        "Judges score “PoC readiness” on whether we thought like a state, not whether we rented 80k licences. "
        "Numbers below are order-of-magnitude for discussion with the mentor and i-Hub, not a tender.",
        st["Body"],
    ))

    story.append(P("8.1  Hardware and software requirements (state design)", st["H2"]))
    story.extend(bullets([
        "Software: Linux, Kubernetes (or first Docker Swarm), Postgres + PostGIS, Redis/NATS, MinIO/S3, FastAPI, React, OpenSearch for events, Keycloak.",
        "AI: NVIDIA L4/L40S class in district GPU rooms; Triton or Ultralytics server; CPU nodes for hash + orchestration.",
        "Client: browser only for operators; no thick VMS replace.",
        "Estimate philosophy: <b>~5–15% of cameras</b> under continuous heavy AI (junctions, borders, watchlist geofence); rest health + on-demand.",
        "80,000 × 0.10 = 8,000 heavy streams. At ~15–25 streams/GPU depending on model = <b>order of 300–500 GPUs statewide</b> if naive; with motion gating and 5 FPS metadata, this can drop by 3–5×. We will present a range, not a fake exact count.",
    ], st))

    story.append(P("8.2  Network and bandwidth planning", st["H2"]))
    story.extend(bullets([
        "Do not backhaul 80k HD streams to Gandhinagar. Keep pixels in district / city DC.",
        "State WAN carries: alerts, thumbnails, hashes, search queries, occasional clip fetch.",
        "Rough: 2 Mbps effective after encode × 8,000 heavy = 16 Gbps if all centralised — unacceptable. Hence edge infer.",
        "Camera onboard checklist: multicast/unicast, NAT, firewall allow-list, QoS for RTSP.",
        "PoC/50-cam: single LAN or organiser VPN is enough.",
    ], st))

    story.append(P("8.3  Storage and retention", st["H2"]))
    story.extend(bullets([
        "Raw NVR video remains with the owning department (30–90 days typical today).",
        "Platform stores: event clips (e.g. 30–120 s) + thumbnails + hashes + metadata.",
        "Alert clips: 180–365 days (policy). Hashes and audit: 7 years class (align with evidence rules / mentor+NFSU).",
        "PII minimisation: plate crops stored; full face gallery only with legal basis.",
    ], st))

    story.append(P("8.4  AI processing capacity", st["H2"]))
    story.extend(bullets([
        "Queue + priority: watchlist geofence &gt; officer rewind &gt; random sample quality audit.",
        "Model zoo: YOLOv8n/s vehicle, plate, optional face; INT8 where accuracy holds.",
        "SLA target (design): watchlist match alert &lt; 5–10 s after the vehicle is readable in frame.",
        "Human confirm before external SMS/dispatch in v1.",
    ], st))

    story.append(P("8.5  Disaster recovery", st["H2"]))
    story.extend(bullets([
        "RPO / RTO (design): registry+watchlist RPO 5–15 min (stream replication); RTO 1–4 h for API.",
        "Active-passive State SOC DB; district ingest can run islanded (local alerts) if WAN dies.",
        "Daily backup of hash chain and watchlists offline.",
        "Chaos test in PoC: kill one worker; cameras stay green/red honestly; no silent drop.",
    ], st))

    story.append(P("8.6  Statewide rollout plan", st["H2"]))
    roll = [
        [P("Wave", H), P("Scope", H), P("Success gate", H)],
        [P("0  Hackathon", C), P("Own feeds + 50-cam test", C), P("Designated vehicle found + GIS route", C)],
        [P("1  One commissionerate", C), P("Ahmedabad or Surat zone, 500–2,000 cams", C), P("SOP live 30 days; false-alert rate logged", C)],
        [P("2  Traffic + highway spine", C), P("ANPR-heavy corridors", C), P("RTO stolen list auto-ingest", C)],
        [P("3  All commissionerate / range", C), P("Registry 100% of known cams even if not AI-on", C), P("Map complete; health SLA", C)],
        [P("4  Remaining districts / ULBs", C), P("Adapters for leftover vendors", C), P("80k identities in registry", C)],
    ]
    story.append(table(roll, [40 * mm, 70 * mm, 70 * mm]))
    story.append(P("Table 10. Rollout: registry coverage first, AI second.", st["Caption"]))

    story.append(P("8.7  Budget plan for scale (the number judges and mentors will remember)", st["H2"]))
    story.append(P(
        "This is a <b>government-style indicative DPR sketch</b> for Step 6 (Hardware, Network, Storage, AI, DR, Rollout). "
        "It is <i>not</i> a student purchase indent and <i>not</i> a vendor quotation. Figures are 2026 India street/DC "
        "order-of-magnitude in INR, GST extra. They exist so the proposal looks funded-and-phased, not “we will use Colab forever”.",
        st["Body"],
    ))

    # Highlight KPI strip
    kpi = [
        [P("<b>STUDENT NOW</b><br/>₹0", H),
         P("<b>HACKATHON PoC</b><br/>₹0–0.15 L", H),
         P("<b>STATE PoC (50–500 cam)</b><br/>₹18–26 Lakh", H),
         P("<b>1 COMMISSIONERATE</b><br/>₹1.4–1.9 Cr", H),
         P("<b>GUJARAT 4-YEAR</b><br/>₹28–38 Cr", H),
         P("<b>AVOIDED (Model 4 VMS)</b><br/>₹200–400 Cr+", H)],
    ]
    kt = Table(kpi, colWidths=[30 * mm, 30 * mm, 32 * mm, 30 * mm, 29 * mm, 29 * mm])
    kt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), HexColor("#0D7377")),
        ("BACKGROUND", (1, 0), (1, 0), HexColor("#115E59")),
        ("BACKGROUND", (2, 0), (2, 0), HexColor("#1E3A5F")),
        ("BACKGROUND", (3, 0), (3, 0), HexColor("#1E3A8A")),
        ("BACKGROUND", (4, 0), (4, 0), NAVY),
        ("BACKGROUND", (5, 0), (5, 0), HexColor("#9A3412")),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("BOX", (0, 0), (-1, -1), 0.4, white),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, white),
    ]))
    story.append(kt)
    story.append(P(
        "Figure A. One-glance budget. Federation + reuse of existing NVRs is the cost story. "
        "Replacing 80,000 VMS licences is the bill we refuse to write.",
        st["Caption"],
    ))

    story.append(P("8.7.1  Phased budget (CAPEX + first-year OPEX)", st["H3"]))
    phb = [
        [P("Wave / what Police buy", H), P("Cameras in play", H), P("CAPEX (indicative)", H),
         P("Year-1 OPEX", H), P("Who pays", H)],
        [P("W0  College / Stage-1 software", C), P("4–8 own + files", C),
         P("<b>₹0</b>", C), P("₹0", C), P("Team laptops", C)],
        [P("W0b  Optional booth cams + SSD", C), P("2 cheap ONVIF", C),
         P("₹0.12–0.18 L", C), P("₹0", C), P("College / SSIP if wanted", C)],
        [P("W1  Official 50-cam live test", C), P("~50 gov feeds", C),
         P("<b>₹0</b> (use organiser GPU/VPN)", C), P("₹0", C), P("GPIC lab", C)],
        [P("W2  State technical PoC (after selection)", C), P("50–500 mixed", C),
         P("<b>₹22 L</b> (band ₹18–26 L)", C), P("₹4–6 L", C), P("i-Hub / challenge / Home IT", C)],
        [P("W3  One commissionerate pilot", C), P("1,500–3,000", C),
         P("<b>₹1.60 Cr</b> (band ₹1.4–1.9 Cr)", C), P("₹28–36 L", C), P("Commissionerate + State", C)],
        [P("W4  Traffic + highway ANPR spine", C), P("+5,000–8,000 hot", C),
         P("₹4.5–6.0 Cr incremental", C), P("₹80 L–1.1 Cr", C), P("Traffic / PWD / GSRDC share", C)],
        [P("W5  Statewide federation (4 years)", C), P("Registry 80,000; AI on ~8–12k hot", C),
         P("<b>₹32 Cr</b> total 4-yr (band ₹28–38 Cr)", C), P("₹6–8 Cr / yr at full run", C), P("Home Dept. phased outlay", C)],
    ]
    story.append(table(phb, [48 * mm, 32 * mm, 42 * mm, 28 * mm, 30 * mm]))
    story.append(P("Table 10A. Phased budget — small cheques first, statewide only after gates in Table 10.", st["Caption"]))

    story.append(P("8.7.2  Where ₹22 lakh PoC money goes (attractive because it is specific)", st["H3"]))
    poc = [
        [P("PoC line item (50–500 cameras, 90 days)", H), P("Qty / note", H), P("₹ Lakh", H)],
        [P("GPU inference server (NVIDIA L40S 48 GB or 2× L4 24 GB)", C), P("1 node, 3-year warranty", C), P("9.5", C)],
        [P("CPU / API / DB node (32–64 core, 256 GB, 10 GbE)", C), P("1", C), P("3.2", C)],
        [P("All-flash / NAS for 30-day event clips + hashes (~80–120 TB raw-class)", C), P("1", C), P("3.8", C)],
        [P("Firewall + jump host + vault + certificates", C), P("shared / virtual", C), P("1.2", C)],
        [P("Integration, onboarding 50–500 streams, SOP, 2-week on-site", C), P("team time monetised", C), P("2.8", C)],
        [P("Training 20 operators + documentation (Gujarati/English)", C), P("—", C), P("0.6", C)],
        [P("Contingency 8%", C), P("spares, extra NIC, HDD fail", C), P("0.9", C)],
        [P("<b>PoC total (mid)</b>", C), P("<b>Ready for designated-vehicle SLA</b>", C), P("<b>22.0</b>", C)],
    ]
    story.append(table(poc, [102 * mm, 52 * mm, 26 * mm]))
    story.append(P("Table 10B. A judge can audit this list. We are not asking the college for it.", st["Caption"]))

    story.append(P("8.7.3  One-commissionerate pilot — ₹1.60 Cr mid case", st["H3"]))
    dist = [
        [P("Pilot line (e.g. Surat or Ahmedabad zone)", H), P("₹ Cr", H)],
        [P("GPU farm (8–12× L4/L40S equivalent) + racks, PDU, 20 kVA UPS share", C), P("0.72", C)],
        [P("K8s / API / PostGIS / OpenSearch / MinIO cluster (3-node HA)", C), P("0.22", C)],
        [P("Network (ToR, 25/40 Gb spine share, VPN concentrator)", C), P("0.10", C)],
        [P("SOC workstations (8) + video wall share + 2FA tokens", C), P("0.08", C)],
        [P("SI / integration 5 months, adapters for 4–6 VMS vendors", C), P("0.28", C)],
        [P("Training, change management, 24×7 first 90 days hypercare", C), P("0.08", C)],
        [P("AMC + onsite spares Year-0 prepaid slice", C), P("0.06", C)],
        [P("Contingency ~8%", C), P("0.06", C)],
        [P("<b>Pilot total (mid)</b>", C), P("<b>1.60</b>", C)],
    ]
    story.append(table(dist, [150 * mm, 30 * mm]))
    story.append(P("Table 10C. Commissionerate cheque — still &lt; 1% of a rip-and-replace VMS programme.", st["Caption"]))

    story.append(P("8.7.4  Four-year statewide TCO (federation) vs the bill we avoid", st["H3"]))
    tco = [
        [P("4-year cost head (indicative)", H), P("SentinelShield federation", H), P("Model 4: new central VMS on 80k", H)],
        [P("Reuse existing NVR / cameras / dark fibre", C), P("₹0 extra (already paid by depts)", C), P("Often forklift + dual-run 18 months", C)],
        [P("VMS / channel licences", C), P("₹0–2 Cr (only connectors)", C), P("₹120–280 Cr (₹15–35k / channel class)", C)],
        [P("GPU + edge infer rooms (8–12 sites)", C), P("₹10–14 Cr", C), P("₹12–18 Cr (still needed for AI)", C)],
        [P("State SOC HA + GIS + registry + search", C), P("₹2.5–3.5 Cr", C), P("₹4–8 Cr (bigger video backhaul)", C)],
        [P("WAN / backhaul of pixels to one city", C), P("Low (metadata + clips)", C), P("₹30–60 Cr+ if naive HD centralise", C)],
        [P("SI, training, AMC, people (4 yr)", C), P("₹12–16 Cr", C), P("₹25–40 Cr", C)],
        [P("<b>4-year envelope</b>", C), P("<b>₹28–38 Cr  (use ₹32 Cr mid)</b>", C), P("<b>₹200–400 Cr+  typical class</b>", C)],
        [P("<b>Cost per registered camera (4 yr)</b>", C), P("<b>≈ ₹4,000</b> (₹32 Cr / 80,000)", C), P("≈ ₹25,000–50,000+", C)],
        [P("<b>Cost per AI-hot camera</b>", C), P("≈ ₹32,000 if 10k hot streams", C), P("Still high + licence stack", C)],
    ]
    story.append(table(tco, [62 * mm, 59 * mm, 59 * mm]))
    story.append(P(
        "Table 10D. Headline for mentor and jury: <b>same 80,000-camera identity + watchlist AI at roughly one-tenth the cost</b> "
        "of buying a new statewide VMS. That is why we chose Hybrid Model 1+3+2.",
        st["Caption"],
    ))

    story.append(P("8.7.5  Annual OPEX at full Gujarat run (steady state)", st["H3"]))
    opex = [
        [P("Yearly operating item", H), P("₹ Cr / year", H), P("Note", H)],
        [P("Power + cooling (GPU rooms, ~0.4–0.7 MW peak class if naive; gated lower)", C), P("1.4–2.2", C), P("Edge gating is a cost control, not only an AI trick", C)],
        [P("AMC 18–22% on hardware + infra software", C), P("1.8–2.4", C), P("4-hour GPU spare SLA in 3 cities", C)],
        [P("Platform SRE + SOC analysts (12–20 people loaded)", C), P("2.0–2.8", C), P("Police staff + one SI bench", C)],
        [P("Model refresh, red-team, NFSU audit, DPDP DPO support", C), P("0.4–0.6", C), P("Yearly accuracy + ethics", C)],
        [P("Cloud burst / DR drills / tape of hash chain", C), P("0.2–0.4", C), P("Mostly on-prem", C)],
        [P("<b>Steady OPEX mid</b>", C), P("<b>≈ ₹6.8 Cr / year</b>", C), P("After Wave 5; not in student year", C)],
    ]
    story.append(table(opex, [88 * mm, 32 * mm, 60 * mm]))
    story.append(P("Table 10E. OPEX is honest — GPUs consume power. Gating 90% of cameras keeps this payable.", st["Caption"]))

    story.append(P("8.7.6  Benefit / ROI (why the budget is attractive, not just cheaper)", st["H3"]))
    roi = [
        [P("Benefit lever", H), P("Conservative annual value (indicative)", H)],
        [P("Officer time: 400 investigators save 25 min/day on rewind / VMS hopping", C),
         P("≈ 1.7 lakh person-hours / yr → ₹25–40 Cr loaded-cost class", C)],
        [P("Faster stolen / wanted vehicle hit (Traffic + CID)", C),
         P("Even 50 extra recoveries/yr can exceed the ₹22 L PoC many times over", C)],
        [P("Avoided false pursuit on looped / frozen camera", C),
         P("One avoided incident (fuel, risk, legal) justifies integrity module", C)],
        [P("Avoided dual VMS licence + training lock-in", C),
         P("₹150 Cr+ option value vs Model 4 (Table 10D)", C)],
        [P("Reusable registry for future 112 / ICCC / disaster apps", C),
         P("One GIS identity for every camera — platform, not a point tool", C)],
    ]
    story.append(table(roi, [88 * mm, 92 * mm]))
    story.append(P(
        "Table 10F. Payback on the ₹22 lakh PoC is designed to be <b>inside one quarter</b> if the live test already "
        "finds designated vehicles. Statewide ₹32 Cr is a <b>multi-year insurance policy</b> against a ₹200 Cr+ rip-out.",
        st["Caption"],
    ))

    story.append(P("8.7.7  Funding map (so mentor sees we are not asking the college for ₹32 Cr)", st["H3"]))
    fund = [
        [P("Need", H), P("Amount", H), P("Natural funder", H)],
        [P("Software + report (now)", C), P("₹0", C), P("Students; OSS", C)],
        [P("Optional 2 cameras", C), P("₹15,000", C), P("SSIP / department imprest / skip", C)],
        [P("Stage-1 → finale GPU hours", C), P("in-kind", C), P("GPIC / i-Hub / NFSU / DA-IICT lab", C)],
        [P("₹22 L PoC kit", C), P("₹18–26 L", C), P("Challenge prize (₹37 L pool exists) + i-Hub seed", C)],
        [P("₹1.6 Cr pilot", C), P("1.4–1.9 Cr", C), P("Commissionerate modernisation / Safe City leftover / M-SIP", C)],
        [P("₹32 Cr / 4 yr state", C), P("phased GRs", C), P("Home Department + GoI Safe City / Nirbhaya-class / state IT", C)],
    ]
    story.append(table(fund, [52 * mm, 38 * mm, 90 * mm]))
    story.append(P("Table 10G. Prize money can literally buy the first real PoC server. College cash stays ₹0.", st["Caption"]))

    story.append(P(
        "<b>Mentor one-liner:</b> we spend nothing to compete; if Gujarat adopts the design, they buy a "
        "<b>₹38.4 crore / 36-month statewide go-live</b> (plus one year stabilise) instead of a "
        "<b>₹200–400 crore VMS replacement</b>, at about <b>₹4,800 per camera all-in</b> — not a new camera estate.",
        st["Body"],
    ))

    story.append(P("8.8  ONE STATE — total cost and time to implement (Gujarat)", st["H2"]))
    story.append(P(
        "This section answers the two questions a DGP / mentor / jury will ask in one breath: "
        "<b>How much for the whole state?</b> and <b>How many months until it is live?</b> "
        "Scope = Gujarat only (~80,000 already-installed cameras). No new camera purchase is included "
        "(cameras are already a sunk departmental cost).",
        st["Body"],
    ))

    # Big answer boxes
    ans = [
        [P("<b>TOTAL COST TO IMPLEMENT IN ONE STATE (GUJARAT)</b><br/><font size='13'>₹ 38.4 crore</font><br/>Build ₹32.0 Cr + first-year statewide hypercare / dual-run ₹6.4 Cr<br/>Band: ₹34–44 Cr &nbsp;|&nbsp; Excludes GST, land, new cameras, existing NVR refresh", H),
         P("<b>TIME TO IMPLEMENT IN THE STATE</b><br/><font size='13'>36 months to go-live</font><br/>Month 0–6 PoC+pilot &nbsp;·&nbsp; 7–18 spine &nbsp;·&nbsp; 19–36 all districts<br/>Then months 37–48 stabilise / AMC. First police value at <b>month 6</b> (one city).", H)],
    ]
    at = Table(ans, colWidths=[90 * mm, 90 * mm])
    at.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), HexColor("#0B3D4A")),
        ("BACKGROUND", (1, 0), (1, 0), HexColor("#1E3A8A")),
        ("TEXTCOLOR", (0, 0), (-1, -1), white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 0.5, TEAL),
    ]))
    story.append(at)
    story.append(P("Figure B. The only two numbers that must appear on a slide: ₹38.4 Cr and 36 months.", st["Caption"]))

    story.append(P("8.8.1  Total state cost — build-up (nothing hidden)", st["H3"]))
    tot = [
        [P("Cost block (Gujarat, one-time + Year-0/1)", H), P("₹ Cr", H), P("% of ₹38.4 Cr", H), P("What it buys", H)],
        [P("A  State PoC kit (folded into B; shown for traceability)", C), P("(0.22)", C), P("—", C), P("Table 10B — not added twice", C)],
        [P("B  First commissionerate pilot (includes A)", C), P("1.80", C), P("4.7%", C), P("Table 10C + buffer — live SOP", C)],
        [P("C  Remaining district / range GPU + HA rooms", C), P("13.50", C), P("35.2%", C), P("Edge infer, no HD backhaul", C)],
        [P("D  State SOC, PostGIS registry, search, IAM, DR site", C), P("3.80", C), P("9.9%", C), P("Gandhinagar + DR in a 2nd city", C)],
        [P("E  Connectors to all major VMS / ONVIF / file-drop", C), P("2.80", C), P("7.3%", C), P("Federation, not new VMS licences", C)],
        [P("F  SI, 80k registry clean-up, GIS gap survey", C), P("5.50", C), P("14.3%", C), P("Largest non-hardware work package", C)],
        [P("G  Training 800+ operators, Gujarati SOP, 112 link", C), P("1.60", C), P("4.2%", C), P("Adoption, not only software", C)],
        [P("H  Security audit, NFSU evidence profile, DPDP", C), P("0.80", C), P("2.1%", C), P("Trust module + legal", C)],
        [P("I  Contingency on B–H", C), P("2.20", C), P("5.7%", C), P("Vendor slip / extra adapter", C)],
        [P("<b>BUILD subtotal (B+C+D+E+F+G+H+I)</b>", C), P("<b>32.00</b>", C), P("<b>83.3%</b>", C), P("1.80+13.50+3.80+2.80+5.50+1.60+0.80+2.20", C)],
        [P("J  Statewide hypercare / dual-run for 12 months", C), P("6.40", C), P("16.7%", C), P("People + AMC + power after go-live", C)],
        [P("<b>TOTAL TO IMPLEMENT ONE STATE</b>", C), P("<b>38.40</b>", C), P("<b>100%</b>", C), P("<b>₹32 Cr build + ₹6.4 Cr Year-1 hold</b>", C)],
        [P("Optional add (not required)", C), P("—", C), P("—", C), P("New cameras, 100% 24×7 AI on all 80k, public 5G backhaul", C)],
    ]
    story.append(table(tot, [78 * mm, 32 * mm, 22 * mm, 48 * mm]))
    story.append(P(
        "Table 10H. <b>Quote ₹38.4 crore</b> as “total cost to implement Gujarat”. "
        "Quote <b>₹32 crore</b> if they ask only for build CAPEX. Quote <b>₹6.8 Cr/year</b> (Table 10E) as run-cost after month 48.",
        st["Caption"],
    ))

    story.append(P("8.8.2  Unit economics for one state", st["H3"]))
    unit = [
        [P("Metric", H), P("Value", H)],
        [P("Cameras in scope (existing Gujarat estate)", C), P("~80,000 (no camera CAPEX in this total)", C)],
        [P("All-in implementation cost / camera (₹38.4 Cr ÷ 80,000)", C), P("<b>₹4,800</b>", C)],
        [P("Build-only / camera (₹32 Cr ÷ 80,000)", C), P("₹4,000", C)],
        [P("Steady run / camera / year (₹6.8 Cr ÷ 80,000)", C), P("≈ ₹850 / year", C)],
        [P("AI-hot streams at go-live (10–15% policy)", C), P("8,000–12,000 cameras under heavy infer", C)],
        [P("Cost vs new statewide VMS (₹250 Cr mid-class)", C), P("<b>~6.5× cheaper</b> to implement", C)],
        [P("GST, inflation buffer if tender slips 12 months", C), P("Add 12–18% in a real DPR; still ≪ Model 4", C)],
    ]
    story.append(table(unit, [100 * mm, 80 * mm]))
    story.append(P("Table 10I. Per-camera story: less than the cost of one indoor dome, for software + AI + integrity on a camera they already own.", st["Caption"]))

    story.append(P("8.8.3  Time to implement in the state — 36-month critical path", st["H3"]))
    story.append(P(
        "Clock starts the day Home Department issues a work order (not from today). "
        "Hackathon / student work is <b>Month −3 to 0</b> and is free. "
        "Police start getting operational value at <b>Month 6</b> (one commissionerate), not only at Month 36.",
        st["Body"],
    ))
    tim = [
        [P("Month", H), P("Phase", H), P("What is live for Police", H), P("Gate to next phase", H)],
        [P("−3 to 0", C), P("Hackathon / HLD (₹0)", C), P("Own-feed + 50-cam test demo", C), P("Selection / in-principle nod", C)],
        [P("1 – 3", C), P("Mobilise + PoC kit", C), P("Official 50–200 streams, watchlist test", C), P("Designated-vehicle SLA met", C)],
        [P("4 – 6", C), P("First commissionerate", C), P("<b>First city live</b> (1.5–3k cams), SOP, 24×7 desk", C), P("False-alert rate in band; DGP review", C)],
        [P("7 – 12", C), P("Traffic + highway spine", C), P("ANPR corridors; RTO stolen list auto", C), P("Plate hit used in real cases", C)],
        [P("13 – 18", C), P("All commissionerates / ranges", C), P("Major cities on map; shared watchlist", C), P("Registry ≥ 40k identities", C)],
        [P("19 – 27", C), P("Remaining districts + ULBs", C), P("Adapters for leftover vendors; file-drop sites", C), P("Registry ≥ 70k", C)],
        [P("28 – 36", C), P("Statewide go-live", C), P("<b>80k in registry</b>; AI on hot set; DR drill passed", C), P("SOC sign-off + NFSU pack used in 1 case", C)],
        [P("37 – 48", C), P("Stabilise (not “build”)", C), P("AMC, tune models, island-mode drills", C), P("Hand to steady OPEX ₹6.8 Cr/yr", C)],
    ]
    story.append(table(tim, [24 * mm, 42 * mm, 62 * mm, 52 * mm]))
    story.append(P("Table 10J. <b>36 months to statewide go-live</b>. Value starts at month 6. Full estate identity at month 36.", st["Caption"]))

    story.append(P("8.8.4  Why not faster / why not slower", st["H3"]))
    story.extend(bullets([
        "<b>Cannot honestly finish a state in 6–9 months:</b> 80,000 rows of dirty GIS, 10+ VMS vendors, district WAN, and training dominate — not Python.",
        "<b>Should not take 6–7 years:</b> federation reuses NVRs; we are not retendering every camera.",
        "<b>Crash programme (24 months)</b> is possible if two commissionerates start in parallel and GIS survey is already clean — add ~15% cost (overtime / dual SI). We do <b>not</b> promise 24 months as the base bid.",
        "<b>People on the clock (indicative):</b> Month 1–6: ~15 engineers + 8 police SMEs. Month 7–36: ~25–35 SI + 12–20 police SOC. Not a 200-person army.",
        "Student team time to a portal-ready prototype remains <b>5 weeks part-time</b> (Table 14) — that is not the state implementation clock.",
    ], st))

    story.append(P("8.8.5  Copy-paste answers for mentor / jury", st["H3"]))
    qa = [
        [P("Question", H), P("Answer we give", H)],
        [P("Total cost to implement in one state?", C),
         P("<b>₹38.4 crore</b> for Gujarat (build ₹32 Cr + Year-1 hypercare ₹6.4 Cr). Band ₹34–44 Cr. No new cameras.", C)],
        [P("Time to implement in the state?", C),
         P("<b>36 months</b> to statewide go-live from work order; <b>first city live in 6 months</b>; 12 more months to stabilise.", C)],
        [P("When do police get value?", C), P("Month 6 — one commissionerate on watchlist + GIS. Not only at the end.", C)],
        [P("Cost if we only do software, no hardware?", C), P("Not a serious state bid. Hardware is ~40% of ₹32 Cr. Software-only is the ₹0 student demo.", C)],
        [P("Can we replicate to another state?", C), P("Same software; new GIS + adapters. Roughly 70–80% of ₹38 Cr, ~30 months, if camera count is similar.", C)],
    ]
    story.append(table(qa, [58 * mm, 122 * mm]))
    story.append(P("Table 10K. Memorise the bold cells. Do not invent a new number on stage.", st["Caption"]))

    # ========== STEP 7 ==========
    story.append(P("9.  STEP 7 — How we will be evaluated (score against official tiles)", st["H1"]))
    ev = [
        [P("Official dimension", H), P("What we will show", H)],
        [P("Successful test case", C), P("Table 8 checklist signed off in rehearsal video.", C)],
        [P("PPT / PDF presentation", C), P("Mentor PDF (this) + 12-slide deck.", C)],
        [P("Solution architecture", C), P("Hybrid 1+3+2, C4 + sequence of a watchlist hit.", C)],
        [P("Working demonstration", C), P("Own-feed always-on backup if gov stream fails.", C)],
        [P("Analytics quality", C), P("Plate read on our Gujarat-format clips; declare OCR accuracy on that set; no fake 99%.", C)],
        [P("Scalability &amp; PoC readiness", C), P("Section 8 numbers + Docker + CSV onboard of 50.", C)],
        [P("Bonus consideration", C), P("Integrity/trust score; UNTRUSTED alert; NFSU-style evidence pack; DPDP note.", C)],
    ]
    story.append(table(ev, [48 * mm, 132 * mm]))
    story.append(P("Table 11. Evaluation mapping — bonus is our differentiator.", st["Caption"]))

    # ========== ZERO COST ==========
    story.append(P("10.  Money — student cash is still ₹0; scale budget lives in §8.7", st["H1"]))
    story.append(P(
        "Do not mix the two envelopes. <b>College / team envelope = ₹0</b> (optional ₹15,000 booth). "
        "<b>Government envelope</b> is the attractive Step-6 plan: ₹22 lakh PoC → ₹1.6 Cr pilot → ₹32 Cr / 4 years, "
        "versus ₹200–400 Cr if Gujarat buys a new 80k-channel VMS.",
        st["Body"],
    ))
    money = [
        [P("Envelope", H), P("Cash", H), P("Notes", H)],
        [P("Now → Stage-1 submission", C), P("<b>₹0</b>", C), P("Laptops, OSS, phone, self-filmed plates, OSM maps", C)],
        [P("Optional expo cameras", C), P("₹0–15,000", C), P("Skip unless mentor wants a physical booth", C)],
        [P("Finale 50-cam live", C), P("₹0 expected", C), P("Organiser feeds + GPU", C)],
        [P("Post-win State PoC kit", C), P("₹18–26 L (mid ₹22 L)", C), P("Table 10B — prize / i-Hub, not college", C)],
        [P("Commissionerate pilot", C), P("₹1.4–1.9 Cr", C), P("Table 10C — after 30-day SOP gate", C)],
        [P("Gujarat — total to implement", C), P("<b>₹38.4 Cr</b>", C), P("₹32 Cr build + ₹6.4 Cr Year-1 hold · Table 10H", C)],
        [P("Gujarat — time to implement", C), P("<b>36 months</b>", C), P("Go-live; first city at month 6 · Table 10J", C)],
    ]
    story.append(table(money, [52 * mm, 42 * mm, 86 * mm]))
    story.append(P("Table 12. Two wallets: students spend nothing; the scale plan is a government product budget.", st["Caption"]))

    # ========== TIME TEAM ==========
    story.append(P("11.  Team, time, and work packages", st["H1"]))
    story.append(P(
        "Event window: challenge expected to start September 2026; Stage 1 open innovation "
        "(students &amp; MSME vs large tech); top six to live finale. We work as student category.",
        st["Body"],
    ))
    team = [
        [P("Role", H), P("Work package", H)],
        [P("Lead / architect", C), P("HLD, model choice Hybrid, mentor comms, submission pack", C)],
        [P("Backend", C), P("Registry, adapters, hash chain, watchlist API, CSV onboard", C)],
        [P("AI", C), P("YOLOv8+track, ANPR, match score, clip crop", C)],
        [P("Frontend + GIS", C), P("React mosaic, Leaflet map, alert inbox, route polyline", C)],
        [P("Cyber + report", C), P("Tamper demos, AES pack, DPDP/ethics, output report, video", C)],
    ]
    story.append(table(team, [40 * mm, 140 * mm]))
    story.append(P("Table 13. Five hats; 4 students can double-up (AI+backend, lead+cyber).", st["Caption"]))

    story.append(P("Calendar if we start immediately (mid-August 2026)", st["H2"]))
    cal = [
        [P("Week", H), P("Output", H)],
        [P("W1", C), P("This mentor sign-off; repo; schema; dummy GIS of 50 Gujarat points", C)],
        [P("W2", C), P("Ingest 4 sources + hash chain + tamper button", C)],
        [P("W3", C), P("ANPR on own clips + watchlist match + alerts", C)],
        [P("W4", C), P("GIS route + searchable events + CSV 50-cam onboard", C)],
        [P("W5", C), P("HLD polish, PPT, 6-min video, ethics page; mock “find this plate” drill", C)],
        [P("Sept+", C), P("Portal submit; then harden for government-feed / finale", C)],
    ]
    story.append(table(cal, [22 * mm, 158 * mm]))
    story.append(P("Table 14. Five focused weeks to a complete Step-5 pack (evenings + weekends).", st["Caption"]))

    # ========== ETHICS ==========
    story.append(P("12.  Ethics, law, and what we will not claim", st["H1"]))
    story.extend(bullets([
        "DPDP Act, 2023: purpose = lawful policing assistance; retention limits; no publishing government faces/plates.",
        "Face watchlist only if legal cell / mentor allows; otherwise vehicles-only for Stage 1 (still satisfies “designated vehicle”).",
        "No claim of 99% ANPR or court-certified evidence; hash chain is a technical aid for NFSU-style custody.",
        "YOLOv8 AGPL: OK for challenge; commercial police production may need licence or model swap — stated in HLD.",
        "Human confirmation before any public-facing alert.",
        "Bias: document OCR weakness on dirty / non-Latin / fancy fonts.",
    ], st))

    # ========== GAP ==========
    story.append(P("13.  Gap analysis vs the portal pictures (nothing left implicit)", st["H1"]))
    gap = [
        [P("Portal item", H), P("In first college idea?", H), P("In this plan?", H)],
        [P("Heterogeneous / multi-VMS / 80k", C), P("No (4 home cams)", C), P("Yes — adapters + scale chapter", C)],
        [P("Model 1 Registry &amp; GIS mandatory", C), P("No", C), P("Yes — first-class module", C)],
        [P("Hybrid vs Model 4", C), P("Implied central app", C), P("Yes — federation chosen", C)],
        [P("Watchlists (stolen, wanted, missing…)", C), P("Partial (face/ANPR toys)", C), P("Yes — schema + matcher", C)],
        [P("All 10 Step-3 tiles", C), P("Only AI + some cyber", C), P("Yes — Sections 4.1–4.10", C)],
        [P("50-cam live + GIS route", C), P("No", C), P("Yes — Table 8", C)],
        [P("Own-feed + gov-feed + HLD + video", C), P("No", C), P("Yes — Table 9", C)],
        [P("DR, bandwidth, retention, rollout", C), P("No", C), P("Yes — Section 8", C)],
        [P("Cyber tamper / hash", C), P("Yes (CyberShield)", C), P("Yes — bonus differentiator", C)],
        [P("Weapon / deepfake as core", C), P("Yes (over-scoped)", C), P("Parked; not the official test case", C)],
    ]
    story.append(table(gap, [62 * mm, 52 * mm, 66 * mm]))
    story.append(P("Table 15. We reshaped the project to the official problem, not the other way around.", st["Caption"]))

    # ========== THESIS ==========
    story.append(P("14.  One-paragraph synopsis (for college file / portal abstract)", st["H1"]))
    story.append(P(
        "SentinelShield is a hybrid statewide CCTV integration platform designed for the Gujarat Police "
        "Innovation Challenge 2026. It implements the mandatory camera Registry and GIS layer, federates "
        "heterogeneous VMS/vendor streams without replacing existing NVRs, and runs AI analytics "
        "(vehicle tracking, Indian ANPR, watchlist matching) only on authenticated video. A cybersecurity "
        "engine maintains SHA-256 hash chains and detects freeze, blackout and replay so that alerts on "
        "tampered feeds are marked untrusted. The prototype is built at zero cash cost on open-source "
        "software and is structured to onboard ~50 mixed cameras, find a designated vehicle, show GIS "
        "movement history, and scale in design to approximately 80,000 cameras by pushing inference to "
        "the edge and keeping raw video with owning departments.",
        st["Body"],
    ))

    # ========== ASK ==========
    story.append(P("15.  Risks if we ignore the official steps", st["H1"]))
    story.extend(bullets([
        "A beautiful YOLO demo with no GIS/registry will fail Step 2 (Model 1 mandatory) and Step 4.",
        "Promising a new central VMS (Model 4) will be marked naïve by police IT.",
        "No watchlist schema ⇒ cannot “identify specified vehicle” under evaluation.",
        "No own-feed backup ⇒ government VPN fails and we have nothing to show.",
        "No scale chapter ⇒ weak on Step 6 / “PoC readiness”.",
    ], st))

    story.append(P("16.  Decision requested from the mentor", st["H1"]))
    story.extend(bullets([
        "Approve project title <b>SentinelShield</b> as the college entry for GPIC 2026 / related internal review.",
        "Approve <b>Hybrid model (1 + 3 + 2)</b> with Model 1 Registry &amp; GIS as week-1 work.",
        "Approve <b>vehicle watchlist + ANPR + GIS route</b> as the primary AI (faces only with written ethics OK).",
        "Approve parking of weapon/deepfake as non-core so we match the live test case.",
        "Approve <b>₹0</b> prototype (no purchase).",
        "Optional: lab GPU slot and a 30-minute mid-review after W3 (first plate match on map).",
        "Nominate / confirm team roles and whether we register as student category on sentinel.gujarat.gov.in.",
    ], st))

    story.append(Spacer(1, 4 * mm))
    sign = [
        [P("<b>Document</b>", C), P("SentinelShield Mentor Briefing — aligned to official Steps 1–7", C)],
        [P("<b>Event</b>", C), P("Gujarat Police Innovation Challenge 2026  ·  sentinel.gujarat.gov.in", C)],
        [P("<b>Date</b>", C), P("18 August 2026", C)],
        [P("<b>Mentor decision</b>", C), P("Approved / Approved with remarks / Revise   (circle)", C)],
        [P("<b>Remarks</b>", C), P(" ", C)],
        [P("<b>Mentor name, dept., signature, date</b>", C), P(" ", C)],
        [P("<b>Team (names / enrolment)</b>", C), P(" ", C)],
    ]
    sg = Table(sign, colWidths=[48 * mm, 132 * mm],
               rowHeights=[7.5*mm, 7.5*mm, 7.5*mm, 8*mm, 18*mm, 18*mm, 16*mm])
    sg.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, SOFT),
        ("BACKGROUND", (0, 0), (0, -1), LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(sg)
    story.append(Spacer(1, 5 * mm))
    story.append(P(
        "Sources for event facts: official portal step structure (team screenshots, 18 Aug 2026); "
        "public reporting on GPIC 2026 (≈80,000 cameras, live feeds, ₹37 lakh prizes, i-Hub / DA-IICT / NFSU, "
        "September start). Infrastructure rupee/GPU figures are indicative design, not vendor quotes. "
        "This is an academic briefing, not a certified police product.",
        st["FooterNote"],
    ))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("Wrote", OUT)


if __name__ == "__main__":
    build()
