"""Image and food content regression tests."""
import re
from pathlib import Path

import pytest
import requests

from conftest import API, BASE_URL

CATEGORY_IMAGE = {
    "Fruits": "fruits.jpg", "Vegetables": "vegetables.jpg", "Grains": "grains.jpg",
    "Pulses": "pulses.jpg", "Nuts": "nuts.jpg", "Seeds": "seeds.jpg", "Dairy": "dairy.jpg",
    "Protein-rich": "protein.jpg", "Traditional": "traditional.jpg",
    "Healthy Snacks": "snacks.jpg", "Beverages": "beverages.jpg",
}

CHECKED_IMAGES = ["/images/hero-dv.jpg", "/images/pillar-manas.jpg"] + \
    [f"/images/food/{v}" for v in sorted(set(CATEGORY_IMAGE.values()))]


@pytest.mark.parametrize("path", CHECKED_IMAGES)
def test_new_artwork_served(path):
    r = requests.get(f"{BASE_URL}{path}", timeout=60)
    assert r.status_code == 200, f"{path} -> {r.status_code}"
    assert r.headers.get("content-type", "").startswith("image/"), r.headers.get("content-type")
    assert len(r.content) > 5000, f"{path} only {len(r.content)} bytes"


def test_food_image_map_covers_all_categories(api_client):
    r = api_client.get(f"{API}/foods", timeout=60)
    assert r.status_code == 200
    foods = r.json()["items"]
    cats = sorted({f["category"] for f in foods})
    missing = [c for c in cats if c not in CATEGORY_IMAGE]
    assert not missing, f"categories with no image mapping: {missing}"
    src = Path("/app/frontend/src/lib/api.js").read_text(encoding="utf-8")
    for cat, img in CATEGORY_IMAGE.items():
        assert cat in src and img in src, f"{cat}->{img} not wired in api.js"


def test_every_food_has_calories(api_client):
    foods = api_client.get(f"{API}/foods", timeout=60).json()["items"]
    assert len(foods) > 30
    bad = [f["name"] for f in foods if not isinstance(f.get("calories"), (int, float))
           or f.get("calories") in (None, 0)]
    assert not bad, f"foods without calories: {bad[:10]}"


def test_no_stock_photo_urls_in_source():
    offenders = []
    for p in list(Path("/app/frontend/src").rglob("*.js*")) + [Path("/app/backend/content.py")]:
        txt = p.read_text(encoding="utf-8", errors="ignore")
        if "unsplash.com" in txt or "pexels.com" in txt:
            offenders.append(str(p))
    assert not offenders, offenders


def test_referenced_images_exist_on_disk():
    pub = Path("/app/frontend/public")
    refs = set()
    for p in list(Path("/app/frontend/src").rglob("*.js*")) + [Path("/app/backend/content.py")]:
        refs |= set(re.findall(r"/images/[A-Za-z0-9_\-/]+\.jpg", p.read_text(encoding="utf-8", errors="ignore")))
    missing = [r for r in refs if not (pub / r.lstrip("/")).exists()]
    assert not missing, missing
