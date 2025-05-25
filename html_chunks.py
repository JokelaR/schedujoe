from datetime import datetime

from models import GameReason, ScheduleDayStatus
from chunk_types import Schedule, Game


html_start = """
<!DOCTYPE html>
<html lang="en">
"""

head = """
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Schedujoe - The Joseph Schedule</title>
        <meta name="description" content="The (non-)authoritative source for the next planned Joseph Anderson stream games.">
        <meta content="Joseph Anderson Stream Schedule" property="og:title" />
        <meta content="What (not *exactly* when) is the next Joe Stream?" property="og:description" />
        <meta content="https://schedujoe.bulder.fi" property="og:url" />
        <meta content="https://schedujoe.bulder.fi/img/thumb.png" property="og:imgage"/>
        <meta name="twitter:image" content="https://schedujoe.bulder.fi/img/thumb.png">
        <meta content="#43B581" data-react-helmet="true" name="theme-color" />
        <link rel="shortcut icon" href="/img/thumb.png" type="image/png">
        <link rel="preload" href="normalize.css" as="style">
        <link rel="preload" href="style.css" as="style">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="normalize.css">
        <link rel="stylesheet" href="style.css">
        <link rel="stylesheet" href="images.css">
    </head>
"""

def schedule_html(schedule: tuple[str, ScheduleDayStatus]) -> str:
    return f'<div title="{schedule[1].to_html_title()}">{schedule[0].capitalize()}</div>\n'

def body_start(schedule: Schedule) -> str:
    return f"""
        <body>
            <h1>Joseph Anderson Stream Schedule</h1>

            <span style="font-size: 1.25rem;">Stream probabilities - Updated {datetime.now().strftime('%d.%m.%y')}{f' - {schedule.extra}' if schedule.extra else ""}</span>
            <div id="scheduleContainer">
                <div id="weekSchedule">
                    {
                        "".join(
                            [schedule_html(day)
                            for day in schedule.days]
                        )
                    }
                </div>
                <div id="dateRange" {'class="hidden"' if schedule.hide_date else ""}>
                    <p class="undernote">{schedule.start}</p>
                    <p class="undernote">{schedule.end}</p>
                </div>    
            </div>
    """

def video_links(game: Game) -> str:
    if game.youtube or game.peertube or game.custom_link:
        string = '<div class="videoLinks">'
        if game.custom_link:
            string += f'<a href="{game.custom_link.url}" title="{game.custom_link.title}"><img src="img/{game.custom_link.icon if game.custom_link.icon else "server-fill.svg"}" alt="{game.custom_link.title}"></a>'
        if game.youtube:
            string += f'<a href="{game.youtube}" title="YouTube{" (Unofficial)" if game.unofficial_vod else ""}"><img src="img/youtube-fill.svg"></a>'
        if game.peertube:
            string += f'<a href="{game.peertube}" title="NodjaTube"><img src="img/server-fill.svg" alt="NodjaTube"></a>'
        string += '</div>'
    else:
        string = ""
    return string

def logo(game: Game) -> str:
    out: str = game.name
    if not game.small_card and not game.ignore_logo:
        if game.custom_logo:
            out = f'<img src="img/{game.custom_logo}" title="{game.name}" alt="{game.name} logo" class="gameLogo" loading="lazy">'
        elif game.steam_id:
            out = f'<img src="https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/{game.steam_id}/logo.png" title="{game.name}" alt="{game.name} logo" class="gameLogo" loading="lazy">'
            
    nest = ""
    if game.nested:
        nest = f"""onclick="toggleHidden([{", ".join([f"'{game}'" for game in game.nested])}])\""""

    return f"""
    <div class="textOverlay" {nest}>
        {out}{f'<span class="note">{game.note}</span>' if game.note else ""}
        {f'<p class="searchableName">{game.name}</p>' if out is not game.name else ""}
    </div>
    """

def background_image(game: Game) -> str:
    html = ""
    if game.steam_id:
        html = f'<img src="https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/{game.steam_id}/library_hero.jpg" class="gameImage" loading="lazy" alt="">'
    if game.image:
        html = f'<img src="img/{game.image}" class="gameImage" loading="lazy" alt="">'
    return html

def game_card(game: Game) -> str:
    if game.is_divider:
        return f'<li class="divider">{game.name}</li>'

    card_classes = ["cardContainer"]
    if game.rating:
        card_classes.append(game.rating.to_html_class())
    if game.small_card:
        card_classes.append("thin")
    if game.reason:
        card_classes.append(game.reason.to_html_class())
    if game.starts_hidden:
        card_classes.append("hidden")
    if game.is_nested:
        card_classes.append("indent")

    # jadseya override
    if game.customID and game.customID == "jadseya":
        card_classes.append("promoBanner")

    card_class = " ".join(card_classes)

    return f"""
        <li {f'id="{game.customID}"' if game.customID else ""} class="{card_class}">
            {background_image(game)}
            <div class="card">
                {logo(game)}
                {video_links(game)}
            </div>
        </li>
    """

def current_games(games: list[Game], secret_games: list[Game]|None = None) -> str:
    return f"""
        <h2>Current games</h2>
        <p>These are the current games Joe is streaming. </p>
        <div id="present">
            <ul>
                {
                    "".join(
                        [game_card(game)
                        for game in games]
                    )
                }
            </ul>
            <div class="horizontal-pair">
                <div id="Secret" class="hidden">
                    <h3>Seasonal Secret</h3>
                    <ul>
                        {
                            "".join(
                                [game_card(game)
                                for game in secret_games]
                            ) if secret_games else ""
                        }
                    </ul>
                </div>
            </div>

            <p>Legend</p>
            <div id="legend">
                <div>
                    <div class="example votingGame"></div>
                    <span>Voted</span>
                </div>
                <div>
                    <div class="example adHoc"></div>
                    <span>Ad Hoc</span>
                </div>
                <div>
                    <div class="example seasonal" onClick="incrementSecret();"></div>
                    <span>Seasonal</span>
                </div>
                <div>
                    <div class="example planned"></div>
                    <span>Planned</span>
                </div>
                <div>
                    <div class="example dropped"></div>
                    <span>Dropped</span>
                </div>
            </div>
    """

def games_category(games: list[Game], title: str, description: str, id: str|None = None, short: bool = True) -> str:
    id = id if id else title.lower().replace(" ", "-").strip(' !?.\n')
    return f"""
        <h2>{title}</h2>
        <p>{description}</p>
        <div id="{id}">
            <ul class="collapsed {"short" if short else ""}">
                {
                    "".join(
                        [game_card(game)
                        for game in games]
                    )
                }
                <button onclick="toggleCollapsed(this)">See More</button>
            </ul>
        </div>
    """

def past_games(games: list[Game]) -> str:
    return f"""
        <h2>Past games</h2>
        <p>These are the voted (and more) games Joe has finished, rated on a four point scale (😀😕😡🤬).</p>
        <p>Note that the ratings are based off of the vibes Joe gives off, and not direct ratings he gives out. Subjectivity is implied.</p>
        <div id="past">
            <ul class="collapsed">
                {
                    "".join(
                        [game_card(game)
                        for game in games]
                    )
                }
                <li class="cardContainer thin"><p class="textOverlay">
                    <a href="https://docs.google.com/spreadsheets/d/1ITQm2xYrVj7sycFsjwPSe8bbCFu3OJmPSGtzm3ZImRE/" title="Spreadsheet for comprehensive stream history">
                        Ancient history
                    </a>
                </li>
                <button onclick="toggleCollapsed(this)">See More</button>
            </ul>
        </div>
    """

def unordered_planned(games: list[Game]) -> str:
    return f"""
        <h2>Unordered planned games</h2>
        <p>These games will probably be played in some order, at some point.</p>
        <div>
            <ul>
                {
                    "".join(
                        [game_card(game)
                        for game in games]
                    )
                }
            </ul>
        </div>
    """

def body_end() -> str:
    return """
            <footer>
                <p>This website covers games Joe has played since the end of the voting game™, starting with Steins;Gate</p>
                <p>Website by Bulder, Joe pointing icon by jelly386, other assets sourced from SteamDB and/or respective games.</p>
                <a href="https://github.com/JokelaR/schedujoe">Hosted on Github Pages</a>
            </footer>
        </body>
        <link rel="stylesheet" disabled="true" id="hypnospaceStyle" href="hypnospace.css">
        <script src="main.js"></script>
    </html>
    """