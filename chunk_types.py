from enum import Enum
import re

from models import GameRating, GameReason, GamesMapping, ScheduleDayStatus

class Schedule:
    def __init__ (self, start: str, end: str, days: list[tuple[str, ScheduleDayStatus]], extra: str|None = None, hide_date: bool = False):
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
                 rating: GameRating|None = None, 
                 steam_id: str|None = None, 
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
    o_games = []
    nesting_ids = set()
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

        o_games.append(Game(
            name,
            game.yt,
            game.pt,
            game.rating,
            game.sid,
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
