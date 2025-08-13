import json
from steam.client import SteamClient
from pydantic import BaseModel
from typing import Literal, TypedDict

class Apps(BaseModel):
    apps: dict[int, 'AppInfo']

class AppInfo(BaseModel):
    common: 'CommonData'

class CommonData(BaseModel):
    library_assets_full: 'LibraryAssetsFull'

class LibraryAssetsFull(BaseModel):
    library_hero: 'Image'
    library_logo: 'Image'

class Image(BaseModel):
    image: dict[Literal['english']|str, str]

class ImageData(TypedDict):
    library_hero: str|None
    library_logo: str|None




def get_app_images(app_ids: list[int]):
    """Generate app info json files"""
    print('[Steam Images] Warming up steam client...')
    client = SteamClient()
    client.anonymous_login()
    print('[Steam Images] Steam client loaded.')

    print(f"[Steam Images] Fetching app images for {app_ids}...")
    infos = client.get_product_info(app_ids)

    if not infos:
        raise ValueError("No app info found for the provided app IDs.")
    
    apps = Apps.model_validate(infos).apps

    images: dict[int, ImageData] = {}
    for id, app in apps.items():
        images[id] = ImageData(
            library_hero=app.common.library_assets_full.library_hero.image.get('english'),
            library_logo=app.common.library_assets_full.library_logo.image.get('english')
        )

    return images

def get_app_images_cached(app_ids: list[int], cache_file: str = 'app_images_cache.json'):
    cached_images: dict[str, ImageData] = {}
    try:
        with open(cache_file, 'r') as f:
            cached_images = json.load(f)
    except FileNotFoundError:
        print(f"[Steam Images] Cache file '{cache_file}' not found. Generating new images.")

    # Check for missing app IDs in the cache
    missing_ids = [app_id for app_id in app_ids if str(app_id) not in cached_images]
    if missing_ids:
        images = get_app_images(missing_ids)
        for app_id, img_data in images.items():
            cached_images[str(app_id)] = img_data

        # Save the updated cache
        with open(cache_file, 'w') as f:
            json.dump(cached_images, f)

    return {id: cached_images[str(id)] for id in app_ids}