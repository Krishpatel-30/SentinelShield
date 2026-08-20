"""Gujarat government CCTV estate — 2 lakh+ cameras (registry counts + sample rows)."""

# Official-feeling design totals (indicative). Real onboarding is by city → area.
CITIES = [
    {"id": "ahmedabad", "name": "Ahmedabad", "lat": 23.0225, "lng": 72.5714, "cameras": 48500,
     "areas": [
         ("east", "East Zone", 23.03, 72.65, 9200),
         ("west", "West Zone", 23.04, 72.51, 8800),
         ("north", "North Zone", 23.10, 72.58, 7100),
         ("south", "South Zone", 22.97, 72.58, 6900),
         ("central", "Central / Walled City", 23.025, 72.58, 5400),
         ("sg_highway", "S.G. Highway", 23.07, 72.51, 4100),
         ("airport", "Airport & SP Ring", 23.07, 72.63, 4000),
         ("naroda", "Naroda–Odhav", 23.07, 72.67, 3000),
     ]},
    {"id": "surat", "name": "Surat", "lat": 21.1702, "lng": 72.8311, "cameras": 32800,
     "areas": [
         ("athwa", "Athwa–Piplod", 21.16, 72.79, 5200),
         ("adajan", "Adajan–Rander", 21.20, 72.79, 4800),
         ("varachha", "Varachha–Kapodra", 21.22, 72.86, 5100),
         ("katargam", "Katargam", 21.21, 72.83, 3600),
         ("udhna", "Udhna–Pandesara", 21.15, 72.85, 4200),
         ("ringroad", "Ring Road / Chowk", 21.19, 72.83, 3900),
         ("sachin", "Sachin–Hazira road", 21.08, 72.88, 2800),
         ("dumas", "Dumas–Coastal", 21.09, 72.72, 3200),
     ]},
    {"id": "vadodara", "name": "Vadodara", "lat": 22.3072, "lng": 73.1812, "cameras": 18600,
     "areas": [
         ("alkapuri", "Alkapuri–Race Course", 22.31, 73.16, 4100),
         ("mandvi", "Mandvi–Walled", 22.30, 73.20, 3600),
         ("gotri", "Gotri–Vasna", 22.32, 73.14, 3400),
         ("manjalpur", "Manjalpur", 22.27, 73.19, 3800),
         ("nizampura", "Nizampura–Sama", 22.34, 73.19, 3700),
     ]},
    {"id": "rajkot", "name": "Rajkot", "lat": 22.3039, "lng": 70.8022, "cameras": 14200,
     "areas": [
         ("kalawad", "Kalawad Road", 22.29, 70.77, 3800),
         ("race", "Race Course", 22.30, 70.80, 3500),
         ("gondalrd", "Gondal Road", 22.27, 70.81, 3400),
         ("university", "University Road", 22.32, 70.80, 3500),
     ]},
    {"id": "gandhinagar", "name": "Gandhinagar", "lat": 23.2156, "lng": 72.6369, "cameras": 9800,
     "areas": [
         ("sec21", "Sector 21 / CHH", 23.22, 72.64, 2800),
         ("infocity", "Infocity–GIFT spur", 23.16, 72.68, 2600),
         ("kh", "KH Road / Pathikashram", 23.23, 72.65, 2200),
         ("capitol", "Capitol Complex", 23.21, 72.63, 2200),
     ]},
    {"id": "bhavnagar", "name": "Bhavnagar", "lat": 21.7645, "lng": 72.1519, "cameras": 7200,
     "areas": [("city", "City & Port", 21.76, 72.15, 4000), ("ghogha", "Ghogha Road", 21.75, 72.18, 3200)]},
    {"id": "jamnagar", "name": "Jamnagar", "lat": 22.4707, "lng": 70.0577, "cameras": 6100,
     "areas": [("city", "City", 22.47, 70.06, 3400), ("refinery", "Refinery belt", 22.40, 69.90, 2700)]},
    {"id": "junagadh", "name": "Junagadh", "lat": 21.5222, "lng": 70.4579, "cameras": 4100,
     "areas": [("city", "City", 21.52, 70.46, 2500), ("girnar", "Girnar road", 21.53, 70.48, 1600)]},
    {"id": "anand", "name": "Anand–Nadiad", "lat": 22.5645, "lng": 72.9289, "cameras": 5400,
     "areas": [("anand", "Anand town", 22.56, 72.93, 2800), ("nadiad", "Nadiad", 22.69, 72.86, 2600)]},
    {"id": "mehsana", "name": "Mehsana", "lat": 23.5880, "lng": 72.3693, "cameras": 4300,
     "areas": [("city", "City", 23.59, 72.37, 4300)]},
    {"id": "bharuch", "name": "Bharuch–Ankleshwar", "lat": 21.7051, "lng": 72.9959, "cameras": 5600,
     "areas": [("bharuch", "Bharuch", 21.71, 73.00, 2800), ("ank", "Ankleshwar GIDC", 21.63, 73.01, 2800)]},
    {"id": "kutch", "name": "Bhuj–Kutch", "lat": 23.2420, "lng": 69.6669, "cameras": 6800,
     "areas": [("bhuj", "Bhuj", 23.24, 69.67, 3000), ("gandhidham", "Gandhidham–Kandla", 23.08, 70.13, 3800)]},
    {"id": "valsad", "name": "Valsad–Vapi", "lat": 20.5992, "lng": 72.9342, "cameras": 5200,
     "areas": [("valsad", "Valsad", 20.61, 72.93, 2400), ("vapi", "Vapi GIDC", 20.39, 72.91, 2800)]},
    {"id": "highway", "name": "State Highways & Checkposts", "lat": 22.5, "lng": 71.8, "cameras": 21400,
     "areas": [
         ("ne1", "NE-1 / Ahmedabad–Vadodara", 22.7, 73.0, 7200),
         ("sh6", "SH-6 coastal", 21.4, 72.7, 6100),
         ("border", "Border & inter-state posts", 24.3, 72.1, 8100),
     ]},
    {"id": "other", "name": "Other districts (pooled)", "lat": 22.3, "lng": 71.2, "cameras": 26900,
     "areas": [
         ("saurashtra", "Rest of Saurashtra", 21.8, 70.8, 11000),
         ("northgj", "North Gujarat rest", 23.8, 72.4, 8900),
         ("tribalsouth", "Dang–Tapi–Narmada", 21.0, 73.6, 7000),
     ]},
]

OWNERS = [
    "Gujarat Police",
    "Municipal Corporation / ULB",
    "R&B / Highway",
    "Home Dept. Safe City",
]

DEMO_CAMS = [
    {"id": "cam-ring", "city": "surat", "area": "ringroad", "name": "Ring Road Junction",
     "lat": 21.1702, "lng": 72.8311, "demo": "ring_road_normal.mp4", "hint": "GJ05AB4321",
     "owner": "Municipal Corporation / ULB", "spot": "Chowk Bazaar signal"},
    {"id": "cam-gate", "city": "surat", "area": "ringroad", "name": "Police HQ Gate",
     "lat": 21.1959, "lng": 72.8302, "demo": "gate_stolen_vehicle.mp4", "hint": "GJ05SS2026",
     "owner": "Gujarat Police", "spot": "Commissionerate gate"},
    {"id": "cam-park", "city": "surat", "area": "athwa", "name": "VR Surat parking",
     "lat": 21.1418, "lng": 72.7709, "demo": "parking_freeze_attack.mp4", "hint": "GJ01CD7788",
     "owner": "Municipal Corporation / ULB", "spot": "Parking deck L2"},
    {"id": "cam-lobby", "city": "surat", "area": "ringroad", "name": "Collector office lobby",
     "lat": 21.1860, "lng": 72.8081, "demo": "lobby_blackout.mp4", "hint": "GJ18XY1100",
     "owner": "Home Dept. Safe City", "spot": "Public lobby"},
]


def total_cameras():
    return sum(c["cameras"] for c in CITIES)


def sample_points(city, area, n=6):
    """A few extra government cameras (registry only, no video) so the area is not empty."""
    import hashlib
    key = f"{city['id']}-{area[0]}"
    pts = []
    for i in range(n):
        h = hashlib.md5(f"{key}-{i}".encode()).hexdigest()
        lat = area[2] + (int(h[:4], 16) % 80 - 40) / 900
        lng = area[3] + (int(h[4:8], 16) % 80 - 40) / 900
        owner = OWNERS[int(h[8], 16) % len(OWNERS)]
        pts.append({
            "id": f"gov-{city['id']}-{area[0]}-{i+1:02d}",
            "name": f"{area[1]} Gov cam {i+1:02d}",
            "spot": f"Pole {100+i} · government owned",
            "lat": round(lat, 5),
            "lng": round(lng, 5),
            "owner": owner,
        })
    return pts
