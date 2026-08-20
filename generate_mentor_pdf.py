#!/usr/bin/env python3
"""Generate mentor briefing PDF for SentinelShield."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, ListFlowable, ListItem, HRFlowable,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = "/home/user/SentinelShield_Mentor_Briefing.pdf"

NAVY = HexColor("#0B1F3A")
TEAL = HexColor("#0D7377")
GOLD = HexColor("#C9A227")
SLATE = HexColor("#334155")
LIGHT = HexColor("#F1F5F9")
SOFT = HexColor("#E2E8F0")
RED = HexColor("#B91C1C")
GREEN = HexColor("#166534")

PAGE_W, PAGE_H = A4


def header_footer(canvas, doc):
    canvas.saveState()
    # top bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 16 * mm, PAGE_W, 16 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H - 17.2 * mm, PAGE_W, 1.2 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Times-Bold", 9)
    canvas.drawString(18 * mm, PAGE_H - 10.5 * mm, "SentinelShield  |  Mentor Briefing")
    canvas.setFont("Times-Roman", 8)
    canvas.drawRightString(PAGE_W - 18 * mm, PAGE_H - 10.5 * mm, "Confidential — Academic / Hackathon Use")

    # footer
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, 12 * mm, PAGE_W, 0.8 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(18 * mm, 5 * mm, "CyberShield CCTV  +  Sentinel-X   ·   Zero-cost prototype")
    canvas.drawRightString(PAGE_W - 18 * mm, 5 * mm, f"Page {doc.page}")
    canvas.restoreState()


def cover_page(canvas, doc):
    header_footer(canvas, doc)
    canvas.saveState()
    # cover band behind title area only on page 1 is handled in flow
    canvas.restoreState()


def styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(
        name="CoverKicker", fontName="Times-Bold", fontSize=10,
        textColor=TEAL, alignment=TA_CENTER, letterSpacing=1.2, spaceAfter=6,
    ))
    s.add(ParagraphStyle(
        name="CoverTitle", fontName="Times-Bold", fontSize=26,
        textColor=NAVY, alignment=TA_CENTER, leading=32, spaceAfter=8,
    ))
    s.add(ParagraphStyle(
        name="CoverSub", fontName="Times-Italic", fontSize=12,
        textColor=SLATE, alignment=TA_CENTER, leading=16, spaceAfter=4,
    ))
    s.add(ParagraphStyle(
        name="H1", fontName="Times-Bold", fontSize=14,
        textColor=NAVY, spaceBefore=12, spaceAfter=6, leading=18,
    ))
    s.add(ParagraphStyle(
        name="H2", fontName="Times-Bold", fontSize=11.5,
        textColor=TEAL, spaceBefore=9, spaceAfter=4, leading=15,
    ))
    s.add(ParagraphStyle(
        name="Body", fontName="Times-Roman", fontSize=10,
        textColor=SLATE, alignment=TA_JUSTIFY, leading=14, spaceAfter=6,
    ))
    s.add(ParagraphStyle(
        name="BulletBody", fontName="Times-Roman", fontSize=10,
        textColor=SLATE, leading=13.5, leftIndent=2,
    ))
    s.add(ParagraphStyle(
        name="Cell", fontName="Times-Roman", fontSize=8.5,
        textColor=SLATE, leading=11.5,
    ))
    s.add(ParagraphStyle(
        name="CellH", fontName="Times-Bold", fontSize=8.5,
        textColor=white, leading=11.5,
    ))
    s.add(ParagraphStyle(
        name="Note", fontName="Times-Italic", fontSize=9,
        textColor=SLATE, leading=12, spaceBefore=4, spaceAfter=6,
    ))
    s.add(ParagraphStyle(
        name="Caption", fontName="Times-Bold", fontSize=9,
        textColor=NAVY, alignment=TA_CENTER, spaceBefore=2, spaceAfter=8,
    ))
    s.add(ParagraphStyle(
        name="FooterNote", fontName="Times-Roman", fontSize=8,
        textColor=SLATE, alignment=TA_CENTER, leading=11,
    ))
    return s


def P(text, style):
    return Paragraph(text, style)


def table(data, col_widths, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    cmds = [
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold") if header else ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY) if header else ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white) if header else ("TEXTCOLOR", (0, 0), (-1, 0), NAVY),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("FONTNAME", (0, 1), (-1, -1), "Times-Roman"),
        ("TEXTCOLOR", (0, 1), (-1, -1), SLATE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.3, SOFT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
    ]
    t.setStyle(TableStyle(cmds))
    return t


def bullets(items, st):
    flow = []
    for it in items:
        flow.append(P("•  " + it, st["BulletBody"]))
    flow.append(Spacer(1, 4))
    return flow


def build():
    st = styles()
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=17 * mm,
        rightMargin=17 * mm,
        topMargin=22 * mm,
        bottomMargin=18 * mm,
        title="SentinelShield — Mentor Briefing",
        author="Project Team",
        subject="Merged CyberShield CCTV and Sentinel-X project explanation",
    )
    C = st["Cell"]
    H = st["CellH"]
    story = []

    # COVER
    story.append(Spacer(1, 8 * mm))
    story.append(P("PROJECT BRIEFING FOR MENTOR", st["CoverKicker"]))
    story.append(P("SentinelShield", st["CoverTitle"]))
    story.append(P("A unified CCTV cybersecurity and AI surveillance platform", st["CoverSub"]))
    story.append(P("Merging <b>CyberShield CCTV</b> and <b>Sentinel-X</b>", st["CoverSub"]))
    story.append(Spacer(1, 4 * mm))

    meta = [
        [P("<b>Document type</b>", C), P("Academic / hackathon mentor note", C),
         P("<b>Date</b>", C), P("18 August 2026", C)],
        [P("<b>Nature</b>", C), P("Zero-cost software prototype", C),
         P("<b>Stack</b>", C), P("Python, OpenCV, YOLOv8, Flask, React", C)],
        [P("<b>Budget</b>", C), P("₹0 (laptops + free tools)", C),
         P("<b>Duration</b>", C), P("Hackathon: 24–36 h · Full MVP: 3–4 months", C)],
    ]
    mt = Table(meta, colWidths=[28 * mm, 58 * mm, 22 * mm, 66 * mm])
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.6, TEAL),
        ("INNERGRID", (0, 0), (-1, -1), 0.2, SOFT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(mt)
    story.append(Spacer(1, 6 * mm))
    story.append(P(
        "<b>One sentence:</b> SentinelShield detects threats in CCTV video <i>and</i> proves "
        "that the video itself was not hacked, frozen, looped, or edited — so a control room "
        "never acts on fake footage.",
        st["Body"],
    ))

    # 1 PURPOSE
    story.append(P("1.  Purpose of this note", st["H1"]))
    story.append(P(
        "This document explains the merged student / hackathon project to a faculty mentor: "
        "why two earlier ideas were combined, what will actually be built, what is deliberately "
        "out of scope, how the work can be done at zero cash cost, and what guidance we request. "
        "It is written so it can be attached to a synopsis, SIH idea note, or internal review.",
        st["Body"],
    ))

    # 2 PROBLEM
    story.append(P("2.  Problem statement", st["H1"]))
    story.append(P(
        "India has a very large installed base of CCTV. Two failures are common and usually treated as separate products:",
        st["Body"],
    ))
    story.append(P("2.1  The feed cannot be trusted (cyber / forensic problem)", st["H2"]))
    story.extend(bullets([
        "Old footage can be <b>looped</b> so a guard sees an empty corridor while an incident happens.",
        "A camera can be <b>frozen</b>, blacked out, or replaced by a file — many NVRs will not flag this.",
        "Clips used as evidence often have <b>no hash chain</b>, so a court or auditor cannot prove integrity.",
        "Default passwords and open RTSP make cameras easy to hijack.",
    ], st))
    story.append(P("2.2  The scene is not understood (AI / operations problem)", st["H2"]))
    story.extend(bullets([
        "Operators cannot watch every screen. Weapons, watch-list faces, and number plates are missed.",
        "Separate apps for ANPR, face, and “AI NVR” do not share one incident picture.",
        "An AI alert on a <b>tampered</b> stream is worse than no alert — it creates false confidence.",
    ], st))
    story.append(P(
        "<b>Mentor takeaway:</b> AI-only CCTV is incomplete. Cyber-only CCTV is incomplete. "
        "The research / product gap is a <b>single pipeline</b> that scores both <i>authenticity</i> and <i>threat</i>.",
        st["Body"],
    ))

    # 3 MERGE
    story.append(P("3.  Why we merged CyberShield and Sentinel-X", st["H1"]))
    story.append(P(
        "Originally two concepts were written. For a hackathon and for a coherent B.Tech / lab story, "
        "they are stronger as one product named <b>SentinelShield</b>.",
        st["Body"],
    ))

    merge_data = [
        [P("Aspect", H), P("CyberShield CCTV", H), P("Sentinel-X", H), P("Merged SentinelShield", H)],
        [P("Question", C), P("Is this video authentic?", C),
         P("What threat is in the scene?", C), P("Is this a real threat on a trusted feed?", C)],
        [P("Core modules", C),
         P("Health monitor, SHA-256 chain, freeze/black/replay, attack rules, alerts", C),
         P("Multi-cam ingest, YOLOv8, face, ANPR, deepfake flag, AES evidence", C),
         P("Ingest + integrity + one or two AI detectors + fusion + dashboard", C)],
        [P("Risk if standalone", C),
         P("Looks like “only hashing” — limited wow factor", C),
         P("Looks like every YOLO demo; ignores spoofed video", C),
         P("Differentiated: red badge if AI fires on untrusted video", C)],
        [P("Role in stack", C), P("Foundation / security layer", C),
         P("Intelligence layer", C), P("One platform, two layers", C)],
    ]
    story.append(table(merge_data, [28 * mm, 48 * mm, 48 * mm, 50 * mm]))
    story.append(P("Table 1. How the two proposals map into one project.", st["Caption"]))

    story.append(P(
        "Recommended academic framing: CyberShield is <b>Work Package A</b> (integrity). "
        "A reduced Sentinel-X is <b>Work Package B</b> (detection). Fusion and the control-room UI "
        "are <b>Work Package C</b>. Deepfake SOTA, city-scale ONVIF, and live police networks stay out of the first prototype.",
        st["Body"],
    ))

    # 4 OBJECTIVES
    story.append(P("4.  Objectives (measurable)", st["H1"]))
    story.append(P("4.1  Primary (must demonstrate)", st["H2"]))
    story.extend(bullets([
        "Ingest at least three sources (webcam and/or video files treated as cameras).",
        "Compute SHA-256 on short segments (about 2–5 seconds) and store a <b>hash chain</b> (each record stores the previous hash).",
        "Detect freeze, black frame, and simple replay/loop within a few seconds and raise a TAMPER alert.",
        "Run YOLOv8 (nano) for person / selected threat class on the same streams.",
        "Fusion rule: if integrity fails, any AI alert is marked <b>UNTRUSTED</b> and must not be treated as evidence.",
        "Export an evidence pack (clip or frames + hashes.json + incident record).",
        "Show a React dashboard with live status badges (trusted / degraded / tampered) and an alert list.",
    ], st))
    story.append(P("4.2  Secondary (if time remains)", st["H2"]))
    story.extend(bullets([
        "Either Indian ANPR (OCR on one still/clip) <b>or</b> a small face watch-list — not both in a 36-hour hackathon.",
        "AES-256 wrapping of the exported clip (software keys).",
        "Telegram bot alert (free) as a stand-in for SMS / police webhook.",
    ], st))
    story.append(P("4.3  Explicitly not claimed in v1", st["H2"]))
    story.extend(bullets([
        "Foolproof deepfake detection (research-grade only; easy to over-claim).",
        "Legal admissibility of evidence without institutional SOP (hashing helps; it is not a court certificate by itself).",
        "City-scale 100-camera GPU cluster.",
        "Replacement of a commercial NVR for a live police control room.",
    ], st))

    # 5 WORKFLOW
    story.append(P("5.  System workflow", st["H1"]))
    story.append(P(
        "Cameras (or virtual cameras) stream into an integration process. Frames go in parallel to "
        "the integrity engine and the AI engine. A fusion service writes incidents. The dashboard "
        "and optional control-room channel consume those incidents.",
        st["Body"],
    ))
    wf = [
        [P("Stage", H), P("Component", H), P("What happens", H)],
        [P("1. Sense", C), P("Phone / file / RTSP", C),
         P("OpenCV or FFmpeg reads frames; camera health (FPS, last-seen) is stored.", C)],
        [P("2. Protect", C), P("CyberShield engine", C),
         P("SHA-256 per segment; chain link; freeze / black / loop scores.", C)],
        [P("3. Understand", C), P("Sentinel-X AI", C),
         P("YOLOv8 (and optional OCR / face) emit labelled boxes and confidence.", C)],
        [P("4. Decide", C), P("Fusion / alerts", C),
         P("Rules combine integrity score + detections → INFO / WARN / CRITICAL / UNTRUSTED.", C)],
        [P("5. Act", C), P("Dashboard", C),
         P("Operator sees mosaic, badges, timeline; downloads court-style pack.", C)],
    ]
    story.append(table(wf, [28 * mm, 42 * mm, 104 * mm]))
    story.append(P("Table 2. End-to-end workflow shown to the mentor and to judges.", st["Caption"]))

    story.append(P(
        "<font face='Courier'>CCTV / files → Ingest → [Hash + Tamper] + [YOLOv8] → Fusion → Flask API → React → Operator</font>",
        st["Note"],
    ))

    # 6 ARCH
    story.append(P("6.  Architecture and technology", st["H1"]))
    story.append(P(
        "The academic specification listed Flask, React, PostgreSQL, OpenCV, SHA-256, YOLOv8, ONVIF, RTSP, and AES. "
        "For a zero-cost prototype we keep the same design and only swap heavy infrastructure for free equivalents.",
        st["Body"],
    ))
    tech = [
        [P("Layer", H), P("Specified", H), P("Zero-cost implementation", H)],
        [P("Ingest", C), P("ONVIF, RTSP, OpenCV", C),
         P("OpenCV on webcam + MP4; optional phone IP Webcam HTTP/RTSP. ONVIF discovery deferred.", C)],
        [P("Integrity", C), P("SHA-256", C),
         P("Python hashlib; HMAC optional; hash chain in SQLite/PostgreSQL.", C)],
        [P("Tamper CV", C), P("OpenCV", C),
         P("Mean luminance, frame-diff, SSIM-style freeze score.", C)],
        [P("Detection", C), P("YOLOv8", C),
         P("Ultralytics YOLOv8n on CPU; Colab only if we fine-tune offline.", C)],
        [P("API", C), P("Flask", C), P("Flask or FastAPI; REST + optional WebSocket.", C)],
        [P("UI", C), P("React", C), P("React + Vite; dark control-room theme.", C)],
        [P("Data", C), P("PostgreSQL", C), P("SQLite for demo; PostgreSQL if Docker is already available (still free).", C)],
        [P("Evidence", C), P("AES", C), P("cryptography AES-GCM on export ZIP; key in env file.", C)],
        [P("Alerts", C), P("Police room", C), P("In-app + optional Telegram bot. No paid SMS.", C)],
    ]
    story.append(table(tech, [28 * mm, 40 * mm, 106 * mm]))
    story.append(P("Table 3. Specification versus zero-cost build.", st["Caption"]))

    story.append(P(
        "<b>Note on weapon class:</b> Stock COCO YOLOv8 does not contain a reliable pistol class. "
        "We will either (a) use a publicly available weapon weight with a cited licence, or "
        "(b) demonstrate person detection plus a small custom class trained on our own clips, "
        "and state this limitation clearly in the report. We will not claim production gun-detection accuracy.",
        st["Body"],
    ))

    # 7 MODULES
    story.append(P("7.  Module list (what the team will code)", st["H1"]))
    mods = [
        [P("ID", H), P("Module", H), P("Origin", H), P("Hackathon?", H), P("Semester MVP?", H)],
        [P("M1", C), P("Camera / file ingest and health", C), P("Both", C), P("Yes", C), P("Yes", C)],
        [P("M2", C), P("SHA-256 segment + hash chain + verify UI", C), P("CyberShield", C), P("Yes", C), P("Yes", C)],
        [P("M3", C), P("Tamper: freeze, black, replay", C), P("CyberShield", C), P("Yes", C), P("Yes", C)],
        [P("M4", C), P("Simple cyber rules (e.g. source change)", C), P("CyberShield", C), P("Light", C), P("Yes", C)],
        [P("M5", C), P("YOLOv8 person / threat", C), P("Sentinel-X", C), P("Yes", C), P("Yes", C)],
        [P("M6", C), P("ANPR or face (pick one)", C), P("Sentinel-X", C), P("If time", C), P("Optional", C)],
        [P("M7", C), P("Deepfake / injection flag", C), P("Sentinel-X", C), P("No (integrity covers injection)", C), P("Basic only", C)],
        [P("M8", C), P("AES evidence pack", C), P("Sentinel-X", C), P("If time", C), P("Yes", C)],
        [P("M9", C), P("Fusion + alerts + React dashboard", C), P("Both", C), P("Yes", C), P("Yes", C)],
    ]
    story.append(table(mods, [16 * mm, 62 * mm, 32 * mm, 42 * mm, 22 * mm]))
    story.append(P("Table 4. Scope control — what we ask the mentor to approve.", st["Caption"]))

    # 8 COST
    story.append(P("8.  Budget — zero cash cost", st["H1"]))
    story.append(P(
        "We request mentor approval to proceed <b>without a purchase indent</b>. "
        "The prototype is designed so that cameras and GPUs are a later deployment step, not a research dependency.",
        st["Body"],
    ))
    cost = [
        [P("Item", H), P("Commercial path", H), P("Our path", H), P("Cash", H)],
        [P("Compute", C), P("Cloud GPU / new RTX", C), P("Team laptops; Colab/Kaggle free if needed", C), P("₹0", C)],
        [P("Cameras", C), P("ONVIF IP cameras", C), P("Phone webcam + our own MP4 clips", C), P("₹0", C)],
        [P("Software", C), P("Licensed NVR / VMS", C), P("Python, OpenCV, React, SQLite — OSS", C), P("₹0", C)],
        [P("Hosting", C), P("AWS / Azure", C), P("Localhost for demo and evaluation", C), P("₹0", C)],
        [P("Alerts", C), P("SMS gateway", C), P("UI + optional free Telegram bot", C), P("₹0", C)],
        [P("Storage", C), P("NAS / S3", C), P("Laptop disk, short clips only", C), P("₹0", C)],
        [P("Total requested", C), P("—", C), P("No department funds for v1", C), P("₹0", C)],
    ]
    story.append(table(cost, [32 * mm, 48 * mm, 78 * mm, 16 * mm]))
    story.append(P("Table 5. Budget. Hardware spend is explicitly deferred.", st["Caption"]))

    story.append(P(
        "If the department later wants a physical lab (not required for evaluation): two inexpensive ONVIF cameras "
        "and cables are about ₹13,000–18,000; a used GPU lab box is a separate ₹50,000-class decision. "
        "We do not ask for this now.",
        st["Body"],
    ))
    story.append(P(
        "<b>Licence honesty:</b> Ultralytics YOLOv8 is typically AGPL-3.0. That is acceptable for a college "
        "and most hackathons. It is not acceptable for a closed commercial fork without a paid licence. "
        "The report will state this. Faces of strangers will not be published in the repository (DPDP / ethics).",
        st["Body"],
    ))

    # 9 TIME
    story.append(P("9.  Time estimate", st["H1"]))
    story.append(P(
        "Time depends on the delivery mode. We ask the mentor to pick one official track so the team is not "
        "graded against a full city platform.",
        st["Body"],
    ))
    time_t = [
        [P("Track", H), P("What is delivered", H), P("Calendar time", H), P("Team", H)],
        [P("A. Hackathon", C),
         P("Merged demo: 3 virtual cameras, hash + tamper, YOLOv8, fusion UI, 3-minute pitch", C),
         P("24–36 hours on site + 3–7 days unpaid prep", C),
         P("3–4 students", C)],
        [P("B. Mini-project / one semester", C),
         P("CyberShield complete + YOLO + dashboard + report (ANPR/face optional)", C),
         P("12–16 weeks part-time (~3–4 months)", C),
         P("2–3 students", C)],
        [P("C. Full Sentinel-X product", C),
         P("Face + ANPR + AES + field cameras + tuning", C),
         P("6–8 months part-time; not a solo semester", C),
         P("4+ students", C)],
    ]
    story.append(table(time_t, [38 * mm, 72 * mm, 42 * mm, 22 * mm]))
    story.append(P("Table 6. Recommended official track is A (hackathon) plus B (semester MVP).", st["Caption"]))

    story.append(P("Suggested semester phases (Track B)", st["H2"]))
    ph = [
        [P("Phase", H), P("Weeks", H), P("Outcome for review", H)],
        [P("P0  Synopsis + threat model + schema", C), P("1", C), P("This briefing + ER sketch", C)],
        [P("P1  Ingest + camera CRUD + health", C), P("2–3", C), P("Three sources on dashboard", C)],
        [P("P2  Hash chain + verify screen", C), P("2–3", C), P("Tamper file fails verify", C)],
        [P("P3  OpenCV tamper detectors", C), P("2", C), P("Freeze / black demo", C)],
        [P("P4  YOLOv8 + fusion alerts", C), P("2–3", C), P("UNTRUSTED vs CRITICAL", C)],
        [P("P5  UI polish, AES export, report", C), P("2–3", C), P("Final demo + PDF report", C)],
    ]
    story.append(table(ph, [70 * mm, 22 * mm, 82 * mm]))
    story.append(P("Table 7. Review checkpoints the mentor can use.", st["Caption"]))

    # 10 EVAL
    story.append(P("10.  How we propose to be evaluated", st["H1"]))
    story.extend(bullets([
        "<b>Live demo (15 min):</b> trusted camera; induced loop/freeze → red badge + hash mismatch; weapon/person clip → box; fusion case “AI on bad video”.",
        "<b>Technical viva:</b> why hash chain, why CPU nano model, DPDP, AGPL, false positives.",
        "<b>Artefacts:</b> GitHub repo, README, this briefing, 10–15 page report, 6-slide pitch.",
        "<b>Metrics (honest):</b> time-to-alert on freeze; hash mismatch on one-bit edit; qualitative YOLO on our clips — not mAP on a private police dataset we do not have.",
    ], st))

    # 11 RISKS
    story.append(P("11.  Risks and ethics (for mentor awareness)", st["H1"]))
    risks = [
        [P("Risk", H), P("Mitigation", H)],
        [P("Over-claiming “court-ready evidence” or “weapon detector 99%”", C),
         P("Language in UI and report: prototype, human confirm, hash helps integrity only.", C)],
        [P("False gun detections (phones, umbrellas)", C),
         P("Operator confirm button; conservative threshold; cite limitation.", C)],
        [P("Face data / DPDP Act, 2023", C),
         P("Prefer no public face module in v1; if used, only consenting teammates; no stranger gallery on GitHub.", C)],
        [P("RTSP / cheap camera pain", C),
         P("Files first; phone stream second; hardware last.", C)],
        [P("Scope creep to full Sentinel-X", C),
         P("Mentor sign-off on Table 4; park face+ANPR+deepfake as future work.", C)],
        [P("Hackathon Wi-Fi failure", C),
         P("Fully offline demo with local MP4s.", C)],
    ]
    story.append(table(risks, [78 * mm, 96 * mm]))
    story.append(P("Table 8. Risks we will write into the report, not hide.", st["Caption"]))

    # 12 ASK
    story.append(P("12.  What we request from the mentor", st["H1"]))
    story.extend(bullets([
        "<b>Approve the merge</b> of CyberShield CCTV and Sentinel-X under the name SentinelShield.",
        "<b>Approve Track A + B scope</b> (Tables 4 and 6) so we are not examined on a 50-camera product.",
        "<b>Approve zero-budget v1</b> (no purchase of cameras or GPU).",
        "Optional: access to a college lab PC if a teammate laptop cannot run YOLOv8n at all (still ₹0).",
        "Optional: a 20-minute mid-review after Phase P2 (hash chain working).",
        "Guidance on whether a face module is ethically acceptable in our department, or should stay out.",
        "If this is aimed at Smart India Hackathon / a police problem statement: help naming a realistic problem code and beneficiary (campus security vs city police).",
    ], st))

    # 13 LEARNING
    story.append(P("13.  Learning outcomes (academic justification)", st["H1"]))
    story.extend(bullets([
        "Applied cryptography: collision-resistant hashing, chain of custody, authenticated export.",
        "Computer vision: classical tamper cues + modern one-stage detection.",
        "Systems: stream ingest, worker processes, REST API, relational schema, role-ready UI.",
        "Security mindset: integrity vs confidentiality vs availability of a camera network.",
        "Professional ethics: biometric data, over-claiming AI, open-source licences.",
    ], st))

    # 14 CLOSING
    story.append(P("14.  Closing summary", st["H1"]))
    story.append(P(
        "SentinelShield is not two half-finished projects. It is one pipeline with a clear thesis: "
        "<b>detect the threat only if the video is authentic</b>. We can demonstrate that thesis on "
        "laptops with free software in a hackathon weekend, then deepen the same code into a "
        "semester MVP. No funds are required to start. We request the mentor’s approval on "
        "name, merge, scope, and zero-cost plan so the team can implement rather than expand slides.",
        st["Body"],
    ))

    story.append(Spacer(1, 6 * mm))
    sign = [
        [P("<b>Prepared for</b>", C), P("Project Mentor / Guide", C)],
        [P("<b>Project title</b>", C), P("SentinelShield — Integrity-aware AI CCTV", C)],
        [P("<b>Decision requested</b>", C),
         P("Approve merge, Track A+B scope, and ₹0 prototype", C)],
        [P("<b>Mentor remarks / signature</b>", C),
         P(" ", C)],
    ]
    sg = Table(sign, colWidths=[45 * mm, 129 * mm], rowHeights=[8 * mm, 8 * mm, 8 * mm, 22 * mm])
    sg.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, SOFT),
        ("BACKGROUND", (0, 0), (0, -1), LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(sg)
    story.append(Spacer(1, 8 * mm))
    story.append(P(
        "This briefing is for academic mentoring. It does not claim a certified police product or legally admissible evidence by itself.",
        st["FooterNote"],
    ))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("Wrote", OUT)


if __name__ == "__main__":
    build()
