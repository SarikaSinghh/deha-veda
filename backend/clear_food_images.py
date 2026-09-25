import asyncio
import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


# ============================================================
# DEHA VEDA — COMPLETE FOOD IMAGE RESET
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"

ENV_FILE = BACKEND_DIR / ".env"
load_dotenv(ENV_FILE)

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "dehaveda")

IMAGE_DIR = FRONTEND_DIR / "public" / "images" / "food" / "items"


async def main():
    print()
    print("=" * 64)
    print("DEHA VEDA — COMPLETE FOOD IMAGE RESET")
    print("=" * 64)
    print()

    client = AsyncIOMotorClient(MONGO_URL)

    try:
        db = client[DB_NAME]

        # --------------------------------------------------------
        # 1. Remove image metadata from EVERY food document
        # --------------------------------------------------------

        result = await db.foods.update_many(
            {},
            {
                "$unset": {
                    "image_url": "",
                    "image_source": "",
                    "image_source_url": "",
                    "image_title": "",
                    "image_match_score": "",
                    "image_license": "",
                    "image_creator": "",
                }
            },
        )

        print(f"MongoDB food documents updated: {result.modified_count}")

        # --------------------------------------------------------
        # 2. Delete all previously downloaded food images
        # --------------------------------------------------------

        deleted_files = 0

        if IMAGE_DIR.exists():
            for item in IMAGE_DIR.iterdir():
                if item.is_file():
                    try:
                        item.unlink()
                        deleted_files += 1
                    except Exception as exc:
                        print(f"Could not delete {item.name}: {exc}")
        else:
            IMAGE_DIR.mkdir(parents=True, exist_ok=True)

        print(f"Local food images deleted       : {deleted_files}")

        # --------------------------------------------------------
        # 3. Delete old Wikimedia/Openverse search cache
        # --------------------------------------------------------

        cache_files = [
            BACKEND_DIR / "food_image_search_cache.json",
            BACKEND_DIR / "openverse_food_cache.json",
        ]

        deleted_caches = 0

        for cache_file in cache_files:
            if cache_file.exists():
                try:
                    cache_file.unlink()
                    deleted_caches += 1
                except Exception as exc:
                    print(f"Could not delete cache {cache_file.name}: {exc}")

        print(f"Old search caches deleted       : {deleted_caches}")

        print()
        print("-" * 64)
        print("RESET COMPLETE")
        print("-" * 64)
        print()
        print("MongoDB image assignments : CLEARED")
        print("Local food images         : CLEARED")
        print("Old search caches         : CLEARED")
        print()
        print("You can now run:")
        print()
        print("    python populate_food_images.py")
        print()

    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())