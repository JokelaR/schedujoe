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
    library_hero: Optional['Image'] = None
    library_logo: Optional['Image'] = None

class Image(BaseModel):
    image: dict[Literal['english']|str, str]

class ImageData(TypedDict):
    library_capsule: str|None
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
        library_capsule = None
        
        if app.common.library_assets_full:
            if app.common.library_assets_full.library_capsule:
                library_capsule = app.common.library_assets_full.library_capsule.image.get('english')
            if app.common.library_assets_full.library_logo:
                library_logo = app.common.library_assets_full.library_logo.image.get('english')
            if app.common.library_assets_full.library_hero:
                library_hero = app.common.library_assets_full.library_hero.image.get('english')
        
        images[id] = ImageData(
            library_capsule=library_capsule,
            library_hero=library_hero,
            library_logo=library_logo
        )

    return images

ids = [
    1125240,
    1718570,
    619820,
    1320140,
    1332010,
    2185060,
    1299460,
    2001120,
    1771300,
    1054950,
    1584090,
    600480,
    2328650,
    3443380,
    2676840,
    2716400,
    1608290,
    3218530,
    1269640,
    1902960,
    310360,
    3151380,
    2637990,
    2714620,
    2303350,
    1671210,
    1812090,
    2864560,
    2843190,
    2600140,
    1705140,
    410890,
    3483740,
    2408820,
    1903340,
    472870,
    2993780,
    1284190,
    587620,
    1679210,
    2201320,
    1389550,
    526490,
    577480,
    2133760,
    2212670,
    2212670,
    1714580,
    2453160,
    3339880,
    668350,
    2589500,
    1746030,
    2698470,
    1385100,
    2653470,
    2014380,
    2444750,
    2885870,
    2508780,
    2359120,
    1145350,
    940680,
    3293010,
    1004640,
    1034940,
    3478050,
    2074370,
    2451100,
    1901370,
    1432500,
    2415010,
    1243670,
    3415230,
    1959390,
    1880620,
    1698960,
    2220360,
    1395520,
    2748340,
    2968420,
    3036350,
    2058730,
    2280430,
    2754380,
    3273530,
    1960900,
    3527290,
    2416100,
    4083190,
    31270,
    272600,
    1672310,
    359510,
    2701800,
    2552430,
]

images = get_app_images(ids)

# print as csv
print("app_id,library_capsule,library_hero,library_logo")
for id in ids:
    img = images.get(id, {})
    capsule = f'https://shared.steamstatic.com/store_item_assets/steam/apps/{id}/{img.get('library_capsule')}'
    hero = f'https://shared.steamstatic.com/store_item_assets/steam/apps/{id}/{img.get('library_hero')}'
    logo = f'https://shared.steamstatic.com/store_item_assets/steam/apps/{id}/{img.get('library_logo')}'

    print(f"{id},{capsule},{hero},{logo}")