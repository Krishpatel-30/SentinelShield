# SentinelShield — Merged hackathon product
## CyberShield CCTV + Sentinel-X in one demo

**Pitch name:** **SentinelShield**  
*“See the threat. Trust the footage.”*

**One-liner:** One platform that (1) proves CCTV video was not tampered with and (2) detects weapons, plates, and watchlist faces — then alerts a control room.

Hackathon judges hear dozens of “YOLO on CCTV” apps. The **merge is the differentiator**: AI detections are useless if the stream was looped. You show **integrity badge + threat box on the same screen**.

---

## What to merge (and what to cut)

| Keep (must demo) | Cut for 24–36 hours | Later (if 48h leftover) |
|---|---|---|
| RTSP / file / webcam ingest | Real ONVIF discovery | PTZ |
| SHA-256 segment + chain | Hardware TPM / blockchain | Multi-site |
| Freeze / black / replay tamper | Full network IDS / Suricata | VLAN sensor |
| YOLOv8 weapon + person | Custom train from scratch | Fine-tune |
| 1 of: ANPR **or** face (not both) | Deepfake SOTA model | MesoNet |
| AES zip of evidence clip | Vault / KMS | HSM |
| React mosaic + alerts | Police real integration | SMS gateway |
| Fusion rule: tamper **or** weapon → CRITICAL | 50 cameras | Map of city |

**Hackathon workflow (merged):**

```
Phone / IP cam / video files
        ↓
 Ingest worker (OpenCV/FFmpeg)
        ↓
 ┌──────────────┬─────────────────┐
 Hash chain     YOLOv8 + optional ANPR/face
 SHA-256        (pretrained weights)
 └──────┬───────┴────────┬────────┘
        ↓                ↓
   Integrity score    Threat events
        └──────┬─────────┘
               ↓
     Fusion + Alert engine
               ↓
   React dashboard + “Court pack” download
```

---

## Team & timebox (typical 24–36h hackathon)

**Team of 4 (ideal)**

| Person | 0–6h | 6–18h | 18–end |
|---|---|---|---|
| A Backend | Flask/FastAPI, DB, hash worker | Evidence AES zip | Judge API polish |
| B ML | YOLO on 2 file streams | Weapon + person boxes to API | Thresholds, fewer FPs |
| C Frontend | Grid, badges, alert toast | Live boxes overlay | Pitch UI / dark SOC theme |
| D Story + demo | Problem, police use-case, script | Tamper demo video | Pitch deck + 3-min video |

**If only 2 people:** skip ANPR/face; do integrity + weapon only.

**Pre-hackathon (do this 3–7 days before — this is how you win):**
- Repo + Docker already running
- YOLOv8n `.pt` downloaded
- 4 demo clips: normal, freeze/loop, gun, number plate
- React shell with dummy cameras
- 3-minute pitch script memorized

If you start from zero *on* hackathon day, you will only finish a half-broken webcam demo.

---

## Demo script (3 minutes — judges)

1. **Problem (20s):** Looping old footage fools guards; AI alone cannot see that.
2. **Live grid:** 3 cameras. Cam-1 green TRUSTED.  
3. **Attack:** You pause / loop Cam-2 → badge RED, hash mismatch, alert “VIDEO TAMPER”.  
4. **Threat:** Play weapon clip on Cam-3 → YOLO box + CRITICAL.  
5. **Fusion:** If both happen → “UNTRUSTED THREAT — do not use as evidence”.  
6. **Court pack:** Download ZIP (clip + `hashes.json` + AES note).  
7. **Ask:** Pilot for campus / police control room.

---

## Money — what you actually spend

All figures **INR, India, Aug 2026**, GST extra where you buy goods.  
**Hackathon prize entry fees vary** — add your event fee on top.

### Tier 0 — Win the hackathon on ₹0–₹2,000 (recommended)

Use what you already have. **Do not buy a GPU or cameras for a weekend event.**

| Item | Cost | Notes |
|---|---|---|
| Laptops (team) | ₹0 | Already owned |
| Video sources | ₹0 | Phone IP Webcam / DroidCam, MP4 files |
| YOLO weights | ₹0 | Ultralytics YOLOv8n (AGPL — check prize rules) or Apache-licensed alt if required |
| Colab / Kaggle GPU | ₹0 | Inference offline clips if laptop is weak |
| Domain (optional) | ₹0 | localhost + ngrok free |
| GitHub + Vercel/Render free | ₹0 | |
| Electricity / snacks / travel | ₹500–2,000 | Real “spend” for most teams |
| SMS / Twilio | ₹0 | Skip; in-app + email only |
| **Total cash** | **₹0–2,000** | |

This is enough to **win** if the story + demo is clean.

### Tier 1 — Strong campus demo after the hackathon (₹8,000–₹25,000)

Buy only if you will **keep building** (SIH finals, college expo, police visit).

| Item | Qty | Unit (approx) | Total |
|---|---|---|---|
| Cheap ONVIF IP camera (Amazon IN ~₹1,300–3,500) | 2 | ₹2,000 | ₹4,000 |
| Ethernet switch + cables | 1 | ₹1,500 | ₹1,500 |
| Domain + cheap VPS (optional, 3 months) | — | — | ₹1,500–3,000 |
| ngrok paid / better tunnel | — | — | ₹0–1,000 |
| Printed posters / standee | — | — | ₹800–2,000 |
| External SSD 1TB (evidence clips) | 1 | ₹4,500–6,000 | ₹5,000 |
| MSG91 SMS test credits | — | — | ₹200–500 |
| **Total** | | | **≈ ₹13,000–18,000** typical |

Skip a new GPU. Use a gaming laptop if anyone has GTX/RTX.

### Tier 2 — Lab / startup prototype (₹40,000–₹1,20,000)

Only if this becomes a **product**, not a hackathon.

| Item | Approx |
|---|---|
| Used RTX 3060 12GB (Nehru Place / OLX class) | ₹22,000–28,000 |
| New/grey 3060-class | ₹25,000–56,000 |
| 4× better ONVIF cams (CP Plus class) | ₹12,000–16,000 |
| Mini PC / used tower if no gaming laptop | ₹15,000–40,000 |
| PoE switch | ₹4,000–8,000 |
| UPS | ₹4,000–8,000 |
| Cloud GPU leftover (RunPod) | ₹1,000–5,000 |
| **Total** | **₹50,000–1,10,000** |

You do **not** need Tier 2 to merge the projects for a hackathon.

### What you should **not** spend on

- New RTX 4070/4080 for a 36-hour event  
- 8 professional cameras  
- Paid YOLO training clusters  
- Blockchain gas / public chain  
- Office, company Pvt Ltd, trademarks (later)

---

## Hidden / non-cash cost (be honest in reports)

| Item | Value |
|---|---|
| 4 students × 30h prep + 36h hack | ~150 hours |
| If you value student time at ₹300/h | ~₹45,000 “effort” |
| Faculty GPU / college lab | often free |
| Pretrained models | free (license risk) |

**Cash vs effort:** cash can be **under ₹2,000**; the real investment is **time**.

---

## Running cost after demo (if you host 24/7)

| | Student | Small pilot (4 cams) |
|---|---|---|
| Electricity (PC+GPU) | laptop only | ₹800–2,000/month |
| VPS | ₹0–500 | ₹800–2,000 |
| Storage 500 GB clips | local disk | ₹0–500 cloud |
| SMS alerts | ₹0 | ₹200–1,000 |
| **Monthly** | **₹0–500** | **₹2,000–5,000** |

---

## Prize / grant angle (India)

- Smart India Hackathon, state police hackathons, MeitY, Gujarat SSIP / i-Hub: budgets often **₹25k–2L** *after* you win — don’t spend that before you have a trophy.
- If a sponsor asks “budget to pilot 10 cameras in a police station,” quote **₹1.5–3.5 lakh** (server + GPU + 10 cams + 2 months on-site), not your hackathon spend.

---

## Recommended merge decision

| Hackathon length | Build | Cash |
|---|---|---|
| 8–12 hours | Integrity + 1 file YOLO + slides | ₹0 |
| **24–36 hours** | **SentinelShield MVP** (hash + tamper + weapon + dashboard) | **₹0–2,000** |
| 48 hours + prep week | + ANPR or face + AES court pack | ₹0–5,000 |
| Post-win prototype | 2 real IP cams + SSD | **₹15,000** |
| Investor / SIH finale hardware | GPU + 4 cams | **₹50,000–80,000** |

**Bottom line:** Merging is the right hackathon story. **Plan to spend almost nothing** (₹0–2,000). Spend ~**₹15,000** only if you will demo real cameras after the event. **₹50,000+** is a lab, not a weekend.

---

## 36-hour build checklist

- [ ] `docker-compose`: API + Postgres + React  
- [ ] 3 video sources (files named `cam1.mp4`…)  
- [ ] Hash every 3 seconds, show hex on UI  
- [ ] Button “Simulate replay attack”  
- [ ] YOLOv8n `person` + `knife`/`gun` if in custom weights, else person + backpack as proxy + label honestly  
- [ ] Alert list + sound  
- [ ] Download `evidence.zip`  
- [ ] README + 6-slide deck  
- [ ] Backup offline demo if Wi-Fi dies  

Weapon class: pretrained COCO has **no reliable gun class**. For hackathon either (a) use a **public weapon YOLOv8 .pt** you downloaded *before* the event, or (b) detect `person` + show “threat zone” with a fine-tuned tiny model you prepared. Do not pretend COCO detects pistols.

---

## One sentence for the registration form

*SentinelShield merges CCTV cybersecurity (SHA-256 integrity, tamper detection) with AI surveillance (YOLOv8 threats) so control rooms only act on video that is both dangerous and authentic.*
