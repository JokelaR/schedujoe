from html_chunks import *
from chunk_types import Status, parse_games
from bs4 import BeautifulSoup
import re

with open('generator_data.txt', 'r') as f:
    data = f.read().split('///')
    # 0: schedule, 1: current games, 2: future games, 3: lock it in, 4: past games, 5: unordered games

#schedule parsing
start = re.search(r"s:(.*)", data[0]).group(1) #type: ignore
end = re.search(r"s:(.*)", data[0]).group(1)   #type: ignore

r_days = re.search(r"Days:\n((?:.*,.*\n)*)", data[0])
if r_days:
    r_days = r_days.group(1).split('\n')
    days: list[tuple[str, Status]] = []
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
    html += current_games(c_games)

#future games parsing
future = re.search(r"Future:\n((?:.*\n)*)", data[2])
if future:
    f_games = parse_games(future)
    html += future_games(f_games)

#lock it in parsing
lock = re.search(r"Lock It In:\n((?:.*\n)*)", data[3])
if lock:
    l_games = parse_games(lock)
    html += lock_it_in(l_games)

#past games parsing
#TODO year separators
past = re.search(r"Past Games:\n((?:.*\n)*)", data[4])
if past:
    p_games = parse_games(past)
    html += past_games(p_games)

#unordered games parsing
unordered = re.search(r"Unordered:\n((?:.*\n)*)", data[5])
if unordered:
    u_games = parse_games(unordered)
    html += unordered_planned(u_games)

html += body_end()

soup = BeautifulSoup(html, 'html.parser')
with open('index.html', 'w', encoding="utf-8") as f:
    f.write(soup.prettify())