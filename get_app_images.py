from steam.client import SteamClient
from pydantic import BaseModel
from typing import Literal, TypedDict, Optional

class Apps(BaseModel):
    apps: dict[int, 'AppInfo']

class AppInfo(BaseModel):
    common: 'CommonData'

class CommonData(BaseModel):
    library_assets_full: Optional['LibraryAssetsFull'] = None

class LibraryAssetsFull(BaseModel):
    library_capsule: Optional['Image'] = None
    library_logo: Optional['Image'] = None

class Image(BaseModel):
    image: dict[Literal['english']|str, str]

class ImageData(TypedDict):
    library_hero: str|None
    library_logo: str|None

client: SteamClient|None = None


def get_app_images(app_ids: list[int]):
    """Generate app info json files"""
    global client

    if not client:
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
        library_hero = None
        library_logo = None
        
        if app.common.library_assets_full:
            if app.common.library_assets_full.library_capsule:
                library_hero = app.common.library_assets_full.library_capsule.image.get('english')
            if app.common.library_assets_full.library_logo:
                library_logo = app.common.library_assets_full.library_logo.image.get('english')
        
        images[id] = ImageData(
            library_hero=library_hero,
            library_logo=library_logo
        )

    return images
