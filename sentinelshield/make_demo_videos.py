#!/usr/bin/env python3
"""Create short recorded demo clips (no copyrighted CCTV)."""
import os
import cv2
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "media", "demos")
os.makedirs(OUT, exist_ok=True)


def put_hud(frame, cam, plate, t, trusted=True):
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (w, 36), (12, 20, 40), -1)
    cv2.putText(frame, f"{cam}  |  {t:05.1f}s  |  {'TRUSTED' if trusted else 'CHECK'}",
                (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (220, 230, 240), 1, cv2.LINE_AA)
    if plate:
        cv2.rectangle(frame, (w - 210, 8), (w - 12, 32), (30, 30, 30), -1)
        cv2.putText(frame, plate, (w - 200, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 220, 255), 2)


def car(frame, x, y, plate):
    cv2.rectangle(frame, (x, y), (x + 120, y + 48), (40, 80, 180), -1)
    cv2.rectangle(frame, (x + 15, y + 8), (x + 50, y + 28), (180, 220, 240), -1)
    cv2.circle(frame, (x + 22, y + 48), 8, (20, 20, 20), -1)
    cv2.circle(frame, (x + 98, y + 48), 8, (20, 20, 20), -1)
    cv2.rectangle(frame, (x + 28, y + 32), (x + 92, y + 46), (250, 250, 250), -1)
    cv2.putText(frame, plate, (x + 30, y + 44), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (10, 10, 10), 1)


def write_clip(path, frames, fps=12):
    h, w = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    vw = cv2.VideoWriter(path, fourcc, fps, (w, h))
    for f in frames:
        vw.write(f)
    vw.release()
    print("wrote", path, "frames", len(frames))


def street_bg(w=640, h=360, shade=0):
    img = np.zeros((h, w, 3), np.uint8)
    img[:] = (48 + shade, 56 + shade, 52 + shade)
    cv2.rectangle(img, (0, 220), (w, h), (70, 70, 70), -1)
    for x in range(0, w, 40):
        cv2.rectangle(img, (x, 268), (x + 22, 276), (200, 200, 200), -1)
    cv2.rectangle(img, (0, 80), (w, 200), (90, 120, 80), -1)
    return img


def demo_normal():
    frames = []
    plate = "GJ05AB4321"
    for i in range(72):
        f = street_bg(shade=i % 3)
        car(f, 20 + i * 7, 230, plate)
        put_hud(f, "CAM-RING-01", plate, i / 12)
        frames.append(f)
    write_clip(os.path.join(OUT, "ring_road_normal.mp4"), frames)


def demo_stolen():
    frames = []
    plate = "GJ05SS2026"
    for i in range(84):
        f = street_bg(shade=2)
        car(f, 10 + i * 6, 228, plate)
        put_hud(f, "CAM-GATE-02", plate, i / 12)
        frames.append(f)
    write_clip(os.path.join(OUT, "gate_stolen_vehicle.mp4"), frames)


def demo_freeze():
    frames = []
    plate = "GJ01CD7788"
    frozen = None
    for i in range(90):
        if i < 30 or i > 70:
            f = street_bg(shade=i % 4)
            car(f, 30 + (i % 40) * 8, 230, plate)
            put_hud(f, "CAM-PARK-03", plate, i / 12, trusted=i < 30)
        else:
            if frozen is None:
                frozen = frames[-1].copy()
            f = frozen.copy()
            put_hud(f, "CAM-PARK-03", "FREEZE?", i / 12, trusted=False)
        frames.append(f)
    write_clip(os.path.join(OUT, "parking_freeze_attack.mp4"), frames)


def demo_blackout():
    frames = []
    for i in range(60):
        if 20 <= i <= 40:
            f = np.zeros((360, 640, 3), np.uint8)
            put_hud(f, "CAM-LOBBY-04", "", i / 12, trusted=False)
        else:
            f = street_bg()
            car(f, 200, 230, "GJ18XY1100")
            put_hud(f, "CAM-LOBBY-04", "GJ18XY1100", i / 12)
        frames.append(f)
    write_clip(os.path.join(OUT, "lobby_blackout.mp4"), frames)


if __name__ == "__main__":
    demo_normal()
    demo_stolen()
    demo_freeze()
    demo_blackout()
