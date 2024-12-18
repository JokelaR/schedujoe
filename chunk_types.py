from enum import Enum
import re

class Status(Enum):
    LIKELY = 'Likely'
    POSSIBLE = 'Possible'
    UNLIKELY = 'Unlikely'
    VERY_UNLIKELY = 'Very unlikely'
    NO_STREAM = 'No stream'

class Schedule:
    def __init__ (self, start: str, end: str, days: list[tuple[str, Status]], hide_date: bool = False):
        self.start = start
        self.end = end
        self.days = days
        self.hide_date = hide_date

class Rating(Enum):
    LOVED = 'loved'
    HATED = 'hated'
    ATROCIOUS = 'atrocious'
    MIXED = 'mixed'
    SKIP = 'skip'
    TROLLEY = 'trolley'

class Reason(Enum):
    ADHOC = 'adHoc'
    SEASONAL = 'seasonal'
    PLANNED = 'planned'
    DROPPED = 'dropped'

class Link:
    def __init__(self, url: str, title: str|None = None, icon: str|None = None):
        self.url = url
        self.title = title
        self.icon = icon

class Game:
    """
    <li id="Wandersong" class="mixed">
        <div class="card">
            <p class="textOverlay">Wandersong</p>
            <div class="videoLinks">
                <a href="https://youtu.be/Wf1BDf1loS4" title="YouTube"><img src="img/youtube-fill.svg" alt="YouTube"></a>
                <a href="https://peertube.nodja.com/w/p/4XzQVVSim7NUv5PiXtA82m" title="NodjaTube"><img src="img/server-fill.svg" alt="NodjaTube"></a>
            </div>
        </div>
    </li>
    """
    def __init__(self, name: str, 
                 youtube: str|None = None, 
                 peertube: str|None = None, 
                 rating: Rating|None = None, 
                 steam_id: str|None = None, 
                 image: str|None = None, 
                 custom_logo: str|None = None,
                 ignore_logo: bool = False,
                 customID: str|None = None, 
                 unofficial_vod: bool = False, 
                 reason: Reason|None = None, 
                 small_card: bool = False, 
                 release_date: str|None = None,
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
        self.image = image
        self.custom_logo = custom_logo
        self.ignore_logo = ignore_logo
        self.customID = customID
        self.reason = reason
        self.small_card = small_card
        self.release_date = release_date
        self.is_divider = is_divider
        self.nested = nested
        self.is_nested = is_nested
        self.custom_link = custom_link
        self.starts_hidden = starts_hidden

def parse_games(games: re.Match[str]) -> list[Game]:
    o_games = []
    nesting_ids = set()
    for game in re.finditer("    (.*\n)((?:        .*\n?)*)", games.group(1)):
        name = game.group(1).strip()
        if name == "":
            continue
        if name[0] == '#':
            name = name[1:]
            o_games.append(Game(name, is_divider=True))
            continue

        reason = re.search(r"\br:(.*)", game.group(2))
        if reason:
            reason = Reason[reason.group(1).strip()]

        youtube = re.search(r"\byt:(.*)", game.group(2))
        if youtube:
            youtube = youtube.group(1).strip()
        peertube = re.search(r"\bpt:(.*)", game.group(2))
        if peertube:
            peertube = peertube.group(1).strip()
        rating = re.search(r"\brating:(.*)", game.group(2))
        if rating:
            rating = Rating[rating.group(1).strip()]

        steam_id = re.search(r"\bsid:(.*)", game.group(2))
        if steam_id:
            steam_id = steam_id.group(1).strip()

        image = re.search(r"\bimg:(.*)", game.group(2))
        if image:
            image = image.group(1).strip()

        custom_logo = re.search(r"\blogo:(.*)", game.group(2))
        if custom_logo:
            custom_logo = custom_logo.group(1).strip()

        customID = re.search(r"\bid:(.*)", game.group(2))
        if customID:
            customID = customID.group(1).strip()

        nested = re.search(r"\bnest:(.*)", game.group(2))
        if nested:
            nested = [game.strip() for game in nested.group(1).split(',')]
            for g in nested:
                nesting_ids.add(g)

        if customID in nesting_ids:
            is_nested = True
        else:
            is_nested = False

        unofficial_vod = re.search(r"\bunofficial_vod", game.group(2)) is not None
        small_card = re.search(r"\bthin", game.group(2)) is not None
        release_date = re.search(r"\brd:(.*)", game.group(2))
        if release_date:
            release_date = release_date.group(1).strip()

        starts_hidden = re.search(r"\bhidden", game.group(2)) is not None
        ignore_logo = re.search(r"\bignore_logo", game.group(2)) is not None

        custom_link = re.search(r"\blink:(.*)\n((?:            .*\n)*)", game.group(2))
        if custom_link:
            url = custom_link.group(1).strip()
            title = re.search(r"\btitle:(.*)", custom_link.group(2))
            if title:
                title = title.group(1).strip()
            icon = re.search(r"\bicon:(.*)", custom_link.group(2))
            if icon:
                icon = icon.group(1).strip()
            custom_link = Link(url, title, icon)

        o_games.append(Game(name, youtube, peertube, rating, steam_id, image, custom_logo, ignore_logo, customID, unofficial_vod, reason, small_card, release_date, starts_hidden, nested, is_nested, custom_link))
    return o_games
