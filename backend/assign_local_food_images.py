"""
Deha Veda — Local Food Image Assigner

Purpose:
    Deterministically assign real local food images to MongoDB food records.

Image location:
    frontend/public/images/food/

Matching:
    Food name <-> image filename

Example:
    "Masala Chai (with milk & sugar)"
        -> "masalachaiwithmilksugar.png"

Rules:
    - No external APIs
    - No web search
    - No fuzzy matching
    - No image deletion
    - Existing valid local images are preserved
    - Safe to run repeatedly
"""

from pathlib import Path
import os
import re
import asyncio

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


# ============================================================
# ENVIRONMENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(BASE_DIR / ".env")


MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "dehaveda")


# ============================================================
# PATHS
# ============================================================

IMAGE_DIR = PROJECT_ROOT / "frontend" / "public" / "images" / "food"


# ============================================================
# SUPPORTED IMAGE EXTENSIONS
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


# ============================================================
# GENERIC CATEGORY IMAGES
#
# These are NOT individual food images.
# ============================================================

GENERIC_CATEGORY_IMAGES = {
    "fruits",
    "vegetables",
    "grains",
    "pulses",
    "nuts",
    "seeds",
    "dairy",
    "protein",
    "traditional",
    "snacks",
    "beverages",
}


# ============================================================
# FILE NAME ALIASES
#
# Only aliases for actual filename mistakes/typos.
#
# Example:
#     pomogranate.png
#     should match
#     Pomegranate
# ============================================================

FILE_ALIASES = {
    "pomogranate": "pomegranate",
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(value: str) -> str:
    """
    Convert food names and filenames into a deterministic
    comparable key.

    Examples:

        "Masala Chai (with milk & sugar)"
            -> "masalachaiwithmilkandsugar"

        "masalachaiwithmilkandsugar.png"
            -> "masalachaiwithmilkandsugar"

        "Pomegranate"
            -> "pomegranate"
    """

    if not value:
        return ""

    value = str(value).strip().lower()

    # Make '&' equivalent to the word "and"
    value = value.replace("&", "and")

    # Remove everything except letters and numbers
    value = re.sub(r"[^a-z0-9]", "", value)

    return value


# ============================================================
# CANONICALIZE IMAGE FILENAMES
# ============================================================

def canonicalize_filename(filename: str) -> str:
    """
    Normalize an image filename and apply known filename aliases.
    """

    key = normalize(filename)

    return FILE_ALIASES.get(key, key)


# ============================================================
# FIND IMAGE FILES
# ============================================================

def find_image_files() -> list[Path]:
    """
    Find individual food images directly inside:

        frontend/public/images/food/

    Generic category images are ignored.
    """

    if not IMAGE_DIR.exists():
        print(f"❌ Image directory does not exist:")
        print(f"   {IMAGE_DIR}")
        return []

    files = []

    for file in IMAGE_DIR.iterdir():

        if not file.is_file():
            continue

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        normalized_name = normalize(file.stem)

        # Ignore generic category images
        if normalized_name in GENERIC_CATEGORY_IMAGES:
            continue

        files.append(file)

    return sorted(files)


# ============================================================
# BUILD IMAGE INDEX
# ============================================================

def build_image_index(image_files: list[Path]) -> dict[str, list[Path]]:
    """
    Build:

        normalized food name -> image file(s)

    Example:

        {
            "apple": [Path("apple.jpg")],
            "banana": [Path("banana.png")],
            "masalachaiwithmilkandsugar": [
                Path("masalachaiwithmilksugar.png")
            ]
        }
    """

    image_index: dict[str, list[Path]] = {}

    for file in image_files:

        key = canonicalize_filename(file.stem)

        if not key:
            continue

        image_index.setdefault(key, []).append(file)

    return image_index


# ============================================================
# CHECK LOCAL IMAGE
# ============================================================

def local_image_exists(image_url: str | None) -> bool:
    """
    Check whether an existing MongoDB image_url points to a
    real local file.
    """

    if not image_url:
        return False

    prefix = "/images/food/"

    if not image_url.startswith(prefix):
        return False

    filename = image_url[len(prefix):]

    # Prevent paths such as:
    # /images/food/../something
    if "/" in filename or "\\" in filename:
        return False

    file_path = IMAGE_DIR / filename

    return file_path.is_file()


# ============================================================
# FIND MATCH
# ============================================================

def find_matching_image(
    food_name: str,
    image_index: dict[str, list[Path]],
):
    """
    Find an exact normalized filename match.

    IMPORTANT:
        No fuzzy matching.
        No guessing.
        No food-name aliases.

    Example:

        DB:
            Masala Chai (with milk & sugar)

        normalize:
            masalachaiwithmilkandsugar

        Image:
            masalachaiwithmilkandsugar.png

        -> MATCH
    """

    food_key = normalize(food_name)

    matches = image_index.get(food_key, [])

    if len(matches) == 1:
        return matches[0], "approved"

    if len(matches) > 1:
        return matches, "ambiguous"

    return None, "missing"


# ============================================================
# UPDATE FOOD
# ============================================================

async def update_food(
    collection,
    food: dict,
    image_file: Path,
):
    """
    Store local image information in MongoDB.
    """

    image_url = f"/images/food/{image_file.name}"

    await collection.update_one(
        {"id": food["id"]},
        {
            "$set": {
                "image_url": image_url,
                "image_source": "local",
                "image_status": "approved",
            },
            "$unset": {
                "image_source_url": "",
                "image_title": "",
                "image_match_score": "",
                "image_license": "",
                "image_creator": "",
            },
        },
    )

    return image_url


# ============================================================
# MAIN
# ============================================================

async def main():

    print()
    print("=" * 70)
    print("DEHA VEDA — LOCAL FOOD IMAGE ASSIGNER")
    print("=" * 70)
    print()

    print(f"MongoDB : {MONGO_URL}")
    print(f"Database: {DB_NAME}")
    print(f"Images  : {IMAGE_DIR}")
    print()

    # --------------------------------------------------------
    # Verify image directory
    # --------------------------------------------------------

    if not IMAGE_DIR.exists():

        print("❌ IMAGE DIRECTORY NOT FOUND")
        print()
        print(f"Expected:")
        print(f"   {IMAGE_DIR}")
        print()

        return

    # --------------------------------------------------------
    # Find images
    # --------------------------------------------------------

    image_files = find_image_files()

    print(f"📷 Images found: {len(image_files)}")
    print()

    if not image_files:

        print("❌ No food images found.")
        return

    # --------------------------------------------------------
    # Build image index
    # --------------------------------------------------------

    image_index = build_image_index(image_files)

    print("IMAGE INDEX")
    print("-" * 70)

    for key, files in sorted(image_index.items()):

        names = ", ".join(file.name for file in files)

        print(f"{key:<45} -> {names}")

    print()

    # --------------------------------------------------------
    # MongoDB
    # --------------------------------------------------------

    client = AsyncIOMotorClient(MONGO_URL)

    try:

        db = client[DB_NAME]
        collection = db.foods

        foods = await collection.find({}).to_list(5000)

        print(f"🍎 Foods found in MongoDB: {len(foods)}")
        print()

        if not foods:

            print("❌ No food records found in MongoDB.")
            return

        # ----------------------------------------------------
        # Counters
        # ----------------------------------------------------

        new_images = 0
        already_assigned = 0
        missing = 0
        ambiguous = 0
        invalid = 0

        missing_foods = []
        ambiguous_foods = []

        # ----------------------------------------------------
        # Process foods
        # ----------------------------------------------------

        for food in foods:

            food_name = food.get("name")
            food_id = food.get("id")

            if not food_name or not food_id:

                invalid += 1

                print(
                    f"⚠ INVALID RECORD -> "
                    f"name={food_name!r}, id={food_id!r}"
                )

                continue

            # ------------------------------------------------
            # Preserve an already valid local image
            # ------------------------------------------------

            existing_image = food.get("image_url")

            if local_image_exists(existing_image):

                already_assigned += 1

                print(
                    f"{food_name:<45} "
                    f"✓ ALREADY ASSIGNED -> {existing_image}"
                )

                continue

            # ------------------------------------------------
            # Find exact image
            # ------------------------------------------------

            result, status = find_matching_image(
                food_name,
                image_index,
            )

            # ------------------------------------------------
            # Approved
            # ------------------------------------------------

            if status == "approved":

                image_url = await update_food(
                    collection,
                    food,
                    result,
                )

                new_images += 1

                print(
                    f"{food_name:<45} "
                    f"✓ ASSIGNED -> {image_url}"
                )

                continue

            # ------------------------------------------------
            # Ambiguous
            # ------------------------------------------------

            if status == "ambiguous":

                ambiguous += 1
                ambiguous_foods.append(
                    (food_name, result)
                )

                print(
                    f"{food_name:<45} "
                    f"⚠ AMBIGUOUS"
                )

                for file in result:
                    print(f"    -> {file.name}")

                continue

            # ------------------------------------------------
            # Missing
            # ------------------------------------------------

            missing += 1
            missing_foods.append(food_name)

            print(
                f"{food_name:<45} "
                f"❌ NO IMAGE FOUND"
            )

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        print()
        print("=" * 70)
        print("FINAL SUMMARY")
        print("=" * 70)

        print(
            f"Total foods           : {len(foods)}"
        )

        print(
            f"New images assigned   : {new_images}"
        )

        print(
            f"Already assigned      : {already_assigned}"
        )

        print(
            f"Missing images        : {missing}"
        )

        print(
            f"Ambiguous matches     : {ambiguous}"
        )

        print(
            f"Invalid records       : {invalid}"
        )

        # ----------------------------------------------------
        # Missing report
        # ----------------------------------------------------

        if missing_foods:

            print()
            print("=" * 70)
            print("MISSING IMAGES")
            print("=" * 70)

            for food_name in missing_foods:

                print(
                    f"❌ {food_name}"
                )

        # ----------------------------------------------------
        # Ambiguous report
        # ----------------------------------------------------

        if ambiguous_foods:

            print()
            print("=" * 70)
            print("AMBIGUOUS IMAGES")
            print("=" * 70)

            for food_name, files in ambiguous_foods:

                print()
                print(f"⚠ {food_name}")

                for file in files:
                    print(f"   -> {file.name}")

        print()
        print("=" * 70)
        print("DONE")
        print("=" * 70)
        print()

    finally:

        client.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())