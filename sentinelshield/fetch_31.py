import urllib.request
import json
import os

url = "https://live.sentinelgujarat.in/api/cameras"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    res = urllib.request.urlopen(req, timeout=10)
    data = json.loads(res.read().decode("utf-8"))
    cams = data.get("cameras", [])
    print(f"Successfully fetched {len(cams)} cameras from sentinelgujarat.in:")
    for c in cams:
        print(f"ID: {c.get('id'):>2s} | Name: {c.get('name'):<12s} | Location: {c.get('location')}")

    with open("sentinel_all_31.json", "w") as f:
        json.dump(cams, f, indent=2)
except Exception as e:
    print(f"Error: {e}")
