# SentinelShield at ₹0
## Yes — the merged project can be built with zero money

**Answer:** For a **hackathon / college project / GitHub demo**, cash can be **₹0**.  
You use laptops you already have, free software, free models, and **video files + phone camera** instead of buying CCTV or a GPU.

You only spend money later if you want **real IP cameras in a building**. That is not required to prove the idea.

---

## What “zero cost” includes

| Need | Free substitute |
|---|---|
| Cameras | Phone (IP Webcam / DroidCam free) + sample MP4s |
| Extra “cameras” | 3–4 downloaded or recorded clips (your own filming) |
| GPU | Laptop CPU + YOLOv8**n** every 3rd frame, **or** Google Colab / Kaggle free GPU |
| Server | `localhost` on your laptop |
| Database | PostgreSQL **or** SQLite (zero install friction) |
| Frontend host | Local Vite, or GitHub Pages / Render / Vercel free |
| Backend host | Local, or Render / Railway / Hugging Face Spaces free tier |
| Hash / AES | Python `hashlib` + `cryptography` (free) |
| YOLO | Ultralytics YOLOv8n pretrained (free download) |
| Face (optional) | InsightFace buffalo_l (free) — heavy; skip if CPU-only |
| ANPR (optional) | EasyOCR / PaddleOCR free — slow on CPU; 1 image demo |
| Alerts | Dashboard toast + browser Notification API (no SMS) |
| Design | Tailwind CSS CDN / npm free |
| Repo | GitHub free |
| OS | Linux / Windows you already have |
| Tunnel for judges | [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) free, or local demo |

**Do not pay for:** domain, Twilio, AWS, new GPU, IP cameras, Figma Pro, ChatGPT Plus.

---

## Zero-cost architecture (hackathon)

```
[Phone webcam] [cam1.mp4] [cam2_loop.mp4] [weapon.mp4]
                      ↓
              Python (FastAPI or Flask)
         ┌────────────┼────────────┐
    SHA-256 chain   OpenCV tamper   YOLOv8n (CPU)
         └────────────┼────────────┘
                      ↓
              SQLite  (hashes, alerts)
                      ↓
              React (Vite) dashboard
```

All on **one laptop**. Second laptop = presenter only.

---

## Software list (all free)

- Python 3.11+, pip  
- `opencv-python`, `ultralytics`, `flask` or `fastapi`, `sqlalchemy`  
- Node.js + React (Vite)  
- FFmpeg (free) if you need RTSP from phone  
- Git + VS Code / Cursor  

Phone app: **IP Webcam** (Android) free → `http://PHONE_IP:8080/video`  
iPhone: use a pre-recorded video if you don’t want a paid app.

---

## What you still fully implement (not a fake project)

Even at ₹0 you can honestly claim:

1. Multi-source ingest (webcam + files as “cameras”)  
2. SHA-256 per segment + hash chain  
3. Tamper: black frame, freeze, file replay  
4. YOLOv8 person / object detection  
5. Fusion alerts (tamper vs threat)  
6. Evidence JSON + clip export  
7. React SOC-style dashboard  

That **is** CyberShield + a sliced Sentinel-X.

---

## What zero cost cannot do (say this in the report)

| Paid / later | Zero-cost workaround |
|---|---|
| 16 real ONVIF cameras | 4 file “virtual cameras” |
| 30 FPS GPU inference | 5–10 FPS on CPU, every 3rd frame |
| Reliable gun class | Pretrained YOLOv8n (COCO) = person, knife is weak; use a **free public weapon .pt** if license allows, or demo person + “restricted object” on your own labelled 20 images (free) |
| SMS to police | On-screen + optional free Telegram bot (BotFather is free) |
| 24/7 server | Demo only when laptop is on |
| Court-grade hardware clock | Software UTC timestamp (good enough for academic) |

Be honest: *“Prototype validated on virtual cameras; hardware cameras are a deployment step, not a research step.”*

---

## GPU without buying one

1. **Best for training / one-off:** Google Colab free T4 — export `best.pt`, run demo on laptop.  
2. **Kaggle** weekly GPU quota — same.  
3. **Hackathon day:** CPU + `yolov8n.pt` (nano). Do not train on site.  
4. If one teammate has any RTX/GTX laptop — use that as the “server”. Still ₹0.

---

## 7-day zero-cost build (before or during long hackathon)

| Day | Output |
|---|---|
| 1 | Flask/FastAPI + SQLite + `/cameras` `/alerts` |
| 2 | OpenCV read webcam + 2 MP4s; health FPS |
| 3 | SHA-256 every 3s; verify endpoint |
| 4 | Freeze + black-frame detector |
| 5 | YOLOv8n on frames; POST boxes to API |
| 6 | React grid, green/red badge, alert list |
| 7 | “Simulate tamper” button, evidence JSON, 3-min pitch |

No shopping. No cloud bill.

---

## Sample clips (free, legal)

- Film your hostel corridor / parking with a phone (you own the copyright).  
- **Do not** download random CCTV of strangers’ faces for a public repo (privacy).  
- Weapon: cardboard/toy in a controlled clip, or public research dataset with license (e.g. some weapon datasets on Kaggle — read license).  
- Loop attack: duplicate 2 seconds of your own video in an editor (DaVinci Resolve free / ffmpeg).

```bash
# freeze / loop a clip with ffmpeg (free)
ffmpeg -stream_loop 20 -i normal.mp4 -c copy cam_replay_attack.mp4
```

---

## Telegram alerts still ₹0

Create a bot with @BotFather, send to your chat. No SMS cost.

---

## Licenses (zero rupees, not zero rules)

- **YOLOv8 / Ultralytics:** AGPL-3.0 unless you buy a license. Fine for college + many hackathons; **bad** if a company wants closed-source. Alternative: YOLOv5 older GPL, or RT-DETR / other Apache models if the event requires it.  
- OpenCV, React, Flask, PostgreSQL/SQLite: permissive.  
- Don’t commit other people’s faces to GitHub.

---

## One-line for judges / synopsis

*SentinelShield is implemented entirely on free and open-source tools and commodity laptops; IP cameras and GPUs are optional deployment upgrades, not required for the integrity + AI pipeline.*

---

## Bottom line

| Question | Answer |
|---|---|
| Can we merge CyberShield + Sentinel-X at zero cost? | **Yes** |
| Will it look like a real product on stage? | **Yes**, if UI + tamper demo + YOLO are tight |
| Must we buy cameras? | **No** |
| Must we buy a GPU? | **No** |
| When does money start? | Only for a **physical site pilot** (~₹15k+), after the hackathon |

**Zero cost is the correct plan for now.**
