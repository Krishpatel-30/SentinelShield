# How to train / upgrade the AI (honest)

The desk **already runs AI continuously** (`engine.py` + background loop):
- freeze / black / loop (OpenCV)
- motion / crowd-rush
- plate match from clip + watchlist
- sightings for **Find vehicle**

That is enough for the hackathon **own-feed** demo.

## What is NOT trained yet (and how you add it later)

### 1) Indian ANPR (YOLOv8 plate + OCR) — official test case

On a PC with a GPU (or Colab free):

```bash
pip install ultralytics paddleocr
# 1. Collect 200–2000 plate photos (your own / public Indian plate sets)
# 2. Label plates in Roboflow or labelImg (class: plate)
# 3. Train:
yolo detect train data=plates.yaml model=yolov8n.pt epochs=50 imgsz=640
# 4. Copy best.pt into sentinelshield/models/plate.pt
```

Then in `engine.py`, replace the filename-hint plate with:
- YOLO detect plate box
- crop
- PaddleOCR / EasyOCR
- `normalize_plate()`

**Do this before the 50-camera government test**, not on the mentor laptop if there is no GPU.

### 2) Vehicle + track

```bash
yolo detect train data=coco.yaml model=yolov8n.pt  # or use coco pretrained car/bus/truck
# ByteTrack is built into ultralytics tracker
```

### 3) Weapon (optional, parked in the PDF)

Only if you have a licensed public weapon dataset. High false positives. Keep human Confirm.

## What you show judges today (no extra training)

1. Cities → Surat → Ring Road  
2. Check video on Police HQ Gate  
3. **Find** `GJ05SS2026` → last seen + map  
4. Alerts: stolen + freeze/black  
5. Help: we do **not** type 2 lakh links  

Continuous AI keeps writing new sightings every ~12 seconds while the server is on.
