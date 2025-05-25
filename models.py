from __future__ import annotations

from datetime import date
from enum import Enum
from io import IOBase
from pprint import pprint
from sys import stdin
from typing import TypeAlias, assert_never
from pydantic import BaseModel, ConfigDict
import yaml

class Model(BaseModel):
    model_config = ConfigDict(extra='forbid')

GamesMapping: TypeAlias = dict[str, "Game"]

class Config(Model):
    schedule: Schedule
    current: GamesMapping|None = None
    dated: GamesMapping|None = None
    future: GamesMapping|None = None
    lock_it_in: GamesMapping|None = None
    past_games: GamesMapping|None = None
    unordered: GamesMapping|None = None
    secret: GamesMapping|None = None


class Schedule(Model):
    hide: bool
    start: date
    end: date
    days: ScheduleDays
    extra: str|None = None


class ScheduleDayStatus(Enum):
    LIKELY = 'LIKELY'
    POSSIBLE = 'POSSIBLE'
    UNLIKELY = 'UNLIKELY'
    VERY_UNLIKELY = 'VERY_UNLIKELY'
    NO_STREAM = 'NO_STREAM'

    def to_html_title(self) -> str:
        if self == ScheduleDayStatus.LIKELY:
            return "Likely"
        if self == ScheduleDayStatus.POSSIBLE:
            return "Possible"
        if self == ScheduleDayStatus.UNLIKELY:
            return "Unlikely"
        if self == ScheduleDayStatus.VERY_UNLIKELY: 
            return "Very unlikely"
        if self == ScheduleDayStatus.NO_STREAM:
            return "No stream"
        assert_never(self)


class ScheduleDays(Model):
    mon: ScheduleDayStatus
    tue: ScheduleDayStatus
    wed: ScheduleDayStatus
    thu: ScheduleDayStatus
    fri: ScheduleDayStatus
    sat: ScheduleDayStatus
    sun: ScheduleDayStatus

class GameReason(str, Enum):
    PLANNED = "PLANNED"
    ADHOC = "ADHOC"
    SEASONAL = "SEASONAL"
    DROPPED = "DROPPED"

    def to_html_class(self) -> str:
        if self == GameReason.PLANNED:
            return "planned"
        if self == GameReason.ADHOC:
            return "adHoc"
        if self == GameReason.SEASONAL:
            return "seasonal"
        if self == GameReason.DROPPED:
            return "dropped"
        assert_never(self)

class GameRating(str, Enum):
    ATROCIOUS = "ATROCIOUS"
    HATED = "HATED"
    MIXED = "MIXED"
    LOVED = "LOVED"
    SKIP = "SKIP"
    DROPPED = "DROPPED"
    TROLLEY = "TROLLEY"

    def to_html_class(self) -> str:
        if self == GameRating.ATROCIOUS:
            return "atrocious"
        if self == GameRating.HATED:
            return "hated"
        if self == GameRating.MIXED:
            return "mixed"
        if self == GameRating.LOVED:
            return "loved"
        if self == GameRating.SKIP:
            return "skip"
        if self == GameRating.DROPPED:
            return "dropped"
        if self == GameRating.TROLLEY:
            return "trolley"
        assert_never(self)

class Game(Model):
    title: str|None = None
    icon: str|None = None
    reason: GameReason|None = None
    rating: GameRating|None = None
    id: str|None = None
    sid: int|None = None
    note: str|None = None
    img: str|None = None
    logo: str|None = None
    thin: bool = False
    ignore_logo: bool = False
    yt: str|None = None
    pt: str|None = None
    unofficial_vod: bool = False
    hidden: bool = False
    nest: list[str] = []
    link: str|None = None
    divider: bool = False

def load_config(data: IOBase) -> Config:
    """
    Load the configuration from a StringIO object containing YAML data.
    """
    unparsed_config = yaml.safe_load(data)
    return Config.model_validate(unparsed_config)

def main():
    pprint(load_config(stdin.read())) # type: ignore

if __name__ == "__main__":
    main()
