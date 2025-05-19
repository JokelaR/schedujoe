from html_chunks import *
from chunk_types import Status, parse_games
from bs4 import BeautifulSoup
import re

with open('generator_data.txt', 'r') as f:
    data = f.read().split('///')
    # 0: schedule, 1: current games, 2: dated, 3: future games, 4: lock it in, 5: past games, 6: unordered games, 7: secret, 

#schedule parsing
start = re.search(r"\bs:(.*)", data[0]).group(1) #type: ignore
end = re.search(r"\be:(.*)", data[0]).group(1)   #type: ignore

r_days = re.search(r"Days:\n((?:.*,.*\n)*)", data[0])
days: list[tuple[str, Status]] = []
if r_days:
    r_days = r_days.group(1).split('\n')
    for day in r_days:
        if len(day) > 0:
            day = day.strip().split(',')
            days.append((day[0], Status[day[1].strip()]))
hide = re.search(r'hide', data[0]) is not None
extra = re.search(r'extra:(.*)', data[0])
if extra:
    extra = extra.group(1).strip()
schedule = Schedule(start, end, days, extra, hide)

html = html_start
html += head
html += body_start(schedule)

#current games parsing
current = re.search(r"Current:\n((?:.*\n)*)", data[1])
if current:
    c_games = parse_games(current)
    secret = re.search(r"Secret:\n((?:.*\n)*)", data[7])
    if secret:
        s_games = parse_games(secret)
        html += current_games(c_games, s_games)
    else:
        html += current_games(c_games)

#date games parsing
dated = re.search(r"Dated:\n((?:.*\n)*)", data[2])
if dated:
    d_games = parse_games(dated)
    html += games_category(
        d_games, 
        title="Dated games", 
        description="These streams are set for a specific date",
        id="dated"
    )

#future games parsing
future = re.search(r"Future:\n((?:.*\n)*)", data[3])
if future:
    f_games = parse_games(future)
    html += games_category(
        f_games, 
        title="Future games", 
        description="These are the Mainstream™ games that will be played roughly in order.",
        id="future"
    )

#lock it in parsing
lock = re.search(r"Lock It In:\n((?:.*\n)*)", data[4])
if lock:
    l_games = parse_games(lock)
    html += games_category(
        l_games, 
        title="Lock It In!", 
        description="These are games that Joe has said he wants to play once they come out. (Dates are for release, not necessarily for when he'll stream them).")

#past games parsing
past = re.search(r"Past Games:\n((?:.*\n)*)", data[5])
if past:
    p_games = parse_games(past)
    html += past_games(p_games)

#unordered games parsing
unordered = re.search(r"Unordered:\n((?:.*\n)*)", data[6])
if unordered:
    u_games = parse_games(unordered)
    html += unordered_planned(u_games)

html += body_end()

soup = BeautifulSoup(html, 'html.parser')
with open('index.html', 'w', encoding="utf-8") as f:
    f.write(soup.prettify())