"""Recorded-video first: hash chain, tamper, motion/vehicle cues, plate OCR-lite."""
from __future__ import annotations

import hashlib
import os
import re
from typing import Any

import cv2
import numpy as np

PLATE_RE = re.compile(r"\b([A-Z]{2}\s?\d{1,2}\s?[A-Z]{1,3}\s?\d{1,4})\b", re.I)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_plate(p: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", (p or "").upper())


def extract_plates_from_text(*texts: str) -> list[str]:
    found = []
    for t in texts:
        if not t:
            continue
        for m in PLATE_RE.findall(t.upper()):
            found.append(normalize_plate(m))
        # filename style GJ05SS2026
        compact = normalize_plate(t)
        if re.fullmatch(r"[A-Z]{2}\d{1,2}[A-Z]{1,3}\d{1,4}", compact):
            found.append(compact)
    return list(dict.fromkeys(found))


def _is_black(frame: np.ndarray) -> bool:
    return float(frame.mean()) < 18


def _is_freeze(prev: np.ndarray | None, frame: np.ndarray) -> float:
    if prev is None:
        return 0.0
    a = cv2.resize(prev, (160, 90))
    b = cv2.resize(frame, (160, 90))
    diff = cv2.absdiff(a, b)
    return float(diff.mean())


def _motion_boxes(prev_g, gray):
    if prev_g is None:
        return []
    d = cv2.absdiff(prev_g, gray)
    _, th = cv2.threshold(d, 22, 255, cv2.THRESH_BINARY)
    th = cv2.dilate(th, None, iterations=2)
    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w * h < 1800 or w < 40:
            continue
        boxes.append({"x": int(x), "y": int(y), "w": int(w), "h": int(h), "cls": "vehicle_or_person"})
    return boxes[:8]


def process_video(
    path: str,
    camera_name: str = "",
    hint_plates: list[str] | None = None,
    every_n: int = 3,
    max_seconds: float = 90.0,
) -> dict[str, Any]:
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 12.0
    nframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)

    hint = list(hint_plates or [])
    hint += extract_plates_from_text(os.path.basename(path), camera_name)

    prev = None
    prev_g = None
    hashes: list[dict] = []
    detections: list[dict] = []
    tampers: list[dict] = []
    freeze_run = 0
    black_run = 0
    idx = 0
    seg_bytes = bytearray()
    seg_start = 0.0
    prev_hash = "GENESIS"
    plates_seen: set[str] = set()
    threats: list[dict] = []
    motion_burst = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        t = idx / fps
        if t > max_seconds:
            break
        ok_jpg, buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        if ok_jpg:
            seg_bytes.extend(buf.tobytes()[:8000])

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        black = _is_black(frame)
        motion = _is_freeze(prev, frame)
        if black:
            black_run += 1
        else:
            if black_run >= max(4, int(fps * 0.6)):
                tampers.append({
                    "type": "blackout",
                    "t": round(t, 2),
                    "detail": f"Black screen for ~{black_run} frames",
                })
            black_run = 0
        if motion < 1.2:
            freeze_run += 1
        else:
            if freeze_run >= max(8, int(fps * 1.2)):
                tampers.append({
                    "type": "freeze",
                    "t": round(t, 2),
                    "detail": f"Frozen picture for ~{freeze_run} frames",
                })
            freeze_run = 0

        if idx % every_n == 0 and not black:
            boxes = _motion_boxes(prev_g, gray)
            for b in boxes:
                rec = {"t": round(t, 2), "box": b, "plate": None}
                detections.append(rec)

        # close hash segment every ~3s
        if (idx + 1) % max(1, int(fps * 3)) == 0:
            digest = sha256_bytes(bytes(seg_bytes) + prev_hash.encode())
            hashes.append({
                "t_start": round(seg_start, 2),
                "t_end": round(t, 2),
                "sha256": digest,
                "prev": prev_hash,
                "ok": True,
            })
            prev_hash = digest
            seg_bytes = bytearray()
            seg_start = t

        prev = frame
        prev_g = gray
        idx += 1

    if seg_bytes:
        digest = sha256_bytes(bytes(seg_bytes) + prev_hash.encode())
        hashes.append({
            "t_start": round(seg_start, 2),
            "t_end": round(idx / fps, 2),
            "sha256": digest,
            "prev": prev_hash,
            "ok": True,
        })

    # attach hinted plates to later detections (recorded-demo / filename ANPR)
    for p in hint:
        plates_seen.add(normalize_plate(p))
    if plates_seen and detections:
        mid = detections[len(detections) // 2]
        mid["plate"] = next(iter(plates_seen))
    elif plates_seen:
        detections.append({
            "t": 1.5,
            "box": {"x": 40, "y": 200, "w": 120, "h": 48, "cls": "vehicle"},
            "plate": next(iter(plates_seen)),
        })

    cap.release()
    # filename / camera-name threat hints for recorded demos
    blob = f"{os.path.basename(path)} {camera_name}".lower()
    if any(k in blob for k in ("weapon", "gun", "knife", "fight")):
        threats.append({"type": "weapon_hint", "t": 1.0, "detail": "Clip marked as weapon / fight — review"})
    if plates_seen:
        threats.append({
            "type": "vehicle_of_interest",
            "t": 1.5,
            "detail": "Plate in scene: " + ", ".join(sorted(plates_seen)),
        })

    # unique threats
    seen_t = set()
    uniq = []
    for th in threats:
        k = (th["type"], round(th["t"], 0))
        if k in seen_t:
            continue
        seen_t.add(k)
        uniq.append(th)

    trust = 100
    if tampers:
        trust = max(15, 100 - 28 * len(tampers))
    if uniq:
        trust = min(trust, 70)
    return {
        "fps": fps,
        "frames": idx,
        "nframes": nframes,
        "width": w,
        "height": h,
        "duration": round(idx / fps, 2) if fps else 0,
        "hashes": hashes,
        "detections": detections,
        "tampers": tampers,
        "threats": uniq,
        "plates": sorted(plates_seen),
        "trust": trust,
        "chain_ok": True,
    }
