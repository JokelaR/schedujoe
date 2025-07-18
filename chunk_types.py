from models import GameRating, GameReason, GamesMapping, ScheduleDays
from datetime import date
import steam_image_utils as steam_img

class Schedule:
    def __init__ (self, start: date, end: date, days: ScheduleDays, extra: str|None = None, hide_date: bool = False):
        self.start = start
        self.end = end
        self.days = days
        self.extra = extra
        self.hide_date = hide_date

class Link:
    def __init__(self, url: str, title: str|None = None, icon: str|None = None):
        self.url = url
        self.title = title
        self.icon = icon

class Game:
    """
    <li class="cardContainer loved planned">
        <img alt="" class="gameImage" loading="lazy" src="https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/1086940/library_hero.jpg">
            <div class="card">
            <div class="textOverlay">
                <img alt="Baldur's Gate 3 logo" class="gameLogo" loading="lazy" src="https://shared.steamstatic.com/store_item_assets/steam/apps/1086940/logo.png" title="Baldur's Gate 3">
                <p class="searchableName">
                Baldur's Gate 3
                </p>
            </div>
            <div class="videoLinks">
                <a href="{youtube}" title="YouTube (Unofficial)">
                    <img src="img/youtube-fill.svg">
                </a>
                <a href="{peertube}" title="NodjaTube">
                    <img alt="NodjaTube" src="img/server-fill.svg">
                </a>
            </div>
        </div>
     </li>
    """
    def __init__(self, name: str, 
                 youtube: str|None = None, 
                 peertube: str|None = None, 
                 rating: GameRating|None = None, 
                 steam_id: int|None = None, 
                 steam_logo: str|None = None,
                 steam_hero: str|None = None,
                 image: str|None = None, 
                 custom_logo: str|None = None,
                 ignore_logo: bool = False,
                 customID: str|None = None, 
                 unofficial_vod: bool = False, 
                 reason: GameReason|None = None, 
                 small_card: bool = False, 
                 note: str|None = None,
                 starts_hidden: bool = False,
                 nested: list[str]|None = None,
                 is_nested: bool = False,
                 custom_link: Link|None = None,
                 is_divider: bool = False
                ):
        self.name = name
        self.rating = rating
        self.youtube = youtube
        self.unofficial_vod = unofficial_vod
        self.peertube = peertube
        self.steam_id = steam_id
        self.steam_logo = steam_logo
        self.steam_hero = steam_hero
        self.image = image
        self.custom_logo = custom_logo
        self.ignore_logo = ignore_logo
        self.customID = customID
        self.reason = reason
        self.small_card = small_card
        self.note = note
        self.is_divider = is_divider
        self.nested = nested
        self.is_nested = is_nested
        self.custom_link = custom_link
        self.starts_hidden = starts_hidden

def parse_games(games: GamesMapping) -> list[Game]:
    o_games: list[Game] = []
    nesting_ids: set[str] = set()
    steam_ids = [game.sid for game in games.values() if game.sid is not None]
    steam_images = steam_img.get_app_images_cached(steam_ids)

    for name, game in games.items():
        if game.divider:
            o_games.append(Game(name, is_divider=True))
            continue

        nested = game.nest
        for g in nested:
            nesting_ids.add(g)

        if game.id in nesting_ids:
            is_nested = True
        else:
            is_nested = False

        custom_link = None
        if game.link:
            title = game.title
            icon = game.icon
            custom_link = Link(game.link, title, icon)
        
        steam_hero: str|None = None
        steam_logo: str|None = None
        if game.sid and steam_images[game.sid]:
            steam_hero = steam_images[game.sid]['library_hero']
            steam_logo = steam_images[game.sid]['library_logo']

        o_games.append(Game(
            name,
            game.yt,
            game.pt,
            game.rating,
            game.sid,
            steam_logo,
            steam_hero,
            game.img,
            game.logo,
            game.ignore_logo,
            game.id,
            game.unofficial_vod,
            game.reason,
            game.thin,
            game.note,
            game.hidden,
            nested,
            is_nested,
            custom_link,
        ))
    return o_games
