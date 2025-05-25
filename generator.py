from html_chunks import body_start, html_start, head, body_end, current_games, games_category, past_games, unordered_planned
from chunk_types import parse_games, Schedule
from bs4 import BeautifulSoup
import re

from models import load_config

with open('generator_data.yaml', 'r') as f:
    config = load_config(f)

_schedule = config.schedule
schedule = Schedule(_schedule.start, _schedule.end, _schedule.days, _schedule.extra, _schedule.hide)

html = html_start
html += head
html += body_start(schedule)

#current games parsing
_current = config.current
if _current:
    c_games = parse_games(_current)
    if config.secret:
        s_games = parse_games(config.secret)
        html += current_games(c_games, s_games)
    else:
        html += current_games(c_games)

#date games parsing
dated = config.dated
if dated:
    d_games = parse_games(dated)
    html += games_category(
        d_games, 
        title="Dated games", 
        description="These streams are set for a specific date",
        id="dated"
    )

#future games parsing
future = config.future
if future:
    f_games = parse_games(future)
    html += games_category(
        f_games, 
        title="Future games", 
        description="These are the Mainstream™ games that will be played roughly in order.",
        id="future"
    )

#lock it in parsing
lock = config.lock_it_in
if lock:
    l_games = parse_games(lock)
    html += games_category(
        l_games, 
        title="Lock It In!", 
        description="These are games that Joe has said he wants to play once they come out. (Dates are for release, not necessarily for when he'll stream them).")

#past games parsing
past = config.past_games
if past:
    p_games = parse_games(past)
    html += past_games(p_games)

#unordered games parsing
unordered = config.unordered
if unordered:
    u_games = parse_games(unordered)
    html += unordered_planned(u_games)

html += body_end()

soup = BeautifulSoup(html, 'html.parser')
with open('index.html', 'w', encoding="utf-8") as f:
    f.write(soup.prettify())
