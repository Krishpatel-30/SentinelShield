# SentinelShield / Sentinel-X Gujarat

One desk: CCTV registry + GIS + demo live clips + AI watchlist + cyber/evidence.

**Do not share Arena / e2b preview links with the team.** Those URLs die when the lab restarts. Share this Git folder instead.

## Run on a laptop

```bash
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 8080
```

Open http://127.0.0.1:8080

| Login    | Password   |
|----------|------------|
| operator | oper123    |
| admin    | admin123   |
| police   | police123  |

Demo plates: `GJ05SS2026` (stolen), `GJ05AB4321`, `GJ27HK9009`.

## Share with the team (GitHub)

One person (first time):

1. Create a **private** repo on GitHub, e.g. `sentinelshield-gujarat`.
2. In this folder:

```bash
git init
git add .
git commit -m "SentinelShield desk"
git branch -M main
git remote add origin https://github.com/YOUR-ORG/sentinelshield-gujarat.git
git push -u origin main
```

3. GitHub → **Settings → Collaborators** → add each teammate.

Everyone else:

```bash
git clone https://github.com/YOUR-ORG/sentinelshield-gujarat.git
cd sentinelshield-gujarat
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 8080
```

Work on **branches**, then pull request. Do not edit the same file at the same time without Git.

## Who edits what

- Desk screens: `static/index.html`, `static/app.js`
- APIs: `app.py`
- Video / plates: `engine.py`
- Cities / camera counts: `gujarat_estate.py`
- TEMP phone test: `static/webcam_test.js`, `static/phone_send.html` (easy to delete)

Do **not** commit real camera passwords or 2 lakh RTSP links.

## Show a demo on one Wi‑Fi

One laptop runs the server. Others open `http://LAPTOP-LAN-IP:8080`.
