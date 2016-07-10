from math import floor

from lxml import etree

from kyokai import Request
from kyokai.blueprints import Blueprint
from kyokai.context import HTTPRequestContext
from kyokai.exc import HTTPException

from owapi import util
from owapi import mo_interface as mo
from owapi import blizz_interface as bz

bp = Blueprint("routes", url_prefix="/api")

PRESTIGE = {
    "0x0250000000000921": 0,
    "0x025000000000094C": 1,
    "0x0250000000000937": 2,
    "0x0250000000000949": 3,
    "0x0250000000000941": 4,
    # 5 will be added once somebody gets it
}


@bp.errorhandler(404)
@util.jsonify
async def a404(ctx: HTTPRequestContext):
    """
    Return a 404 message, probably because the battletag was not found.
    """
    assert isinstance(ctx.request, Request)
    region = ctx.request.values.get("region", None)
    return {"error": 404, "msg": "profile not found", "region": region}, 404


@bp.route("/")
@util.jsonify
async def root(ctx: HTTPRequestContext):
    """
    Return the root message.
    """
    return {}


@bp.route("/v2/u/(.*)/stats/competitive")
@util.jsonify
async def bl_get_compstats(ctx: HTTPRequestContext, battletag: str):
    """
    Get stats for a user using the Blizzard sources.
    """
    data = await bz.region_helper(ctx, battletag, region=ctx.request.values.get("region", None))
    if data == (None, None):
        raise HTTPException(404)

    parsed, region = data

    # Start the dict.
    built_dict = {"region": region, "battletag": battletag, "game_stats": [], "overall_stats": {}, "featured_stats": []}

    # Get the prestige.
    prestige = parsed.xpath(".//div[@class='player-level']")[0]
    # Extract the background-image from the styles.
    try:
        bg_image = [x for x in prestige.values() if 'background-image' in x][0]
    except IndexError:
        # Cannot find background-image.
        # Yikes!
        # Don't set a prestige.
        built_dict["overall_stats"]["prestige"] = 0
    else:
        for key, val in PRESTIGE.items():
            if key in bg_image:
                prestige_num = val
                break
        else:
            # Unknown.
            prestige_num = None
        built_dict["overall_stats"]["prestige"] = prestige_num

    # Parse out the HTML.
    level = int(parsed.findall(".//div[@class='player-level']/div")[0].text)
    built_dict["overall_stats"]["level"] = level

    hasrank = parsed.findall(".//div[@class='competitive-rank']/div")
    if hasrank:
        comprank = int(hasrank[0].text)
    else:
        comprank = None
    built_dict["overall_stats"]["comprank"] = comprank

    hascompstats = parsed.xpath(".//div[@data-group-id='stats' and @data-category-id='0x02E00000FFFFFFFF']")
    if len(hascompstats) != 2:
        return {"error": 404, "msg": "competitive stats not found", "region": region}, 404
    stat_groups = hascompstats[1]

    # Highlight specific stat groups.
    death_box = stat_groups[4]
    game_box = stat_groups[6]

    # Calculate the wins, losses, and win rate.
    wins = int(game_box.xpath(".//text()[. = 'Games Won']/../..")[0][1].text.replace(",", ""))
    g = game_box.xpath(".//text()[. = 'Games Played']/../..")
    games = int(g[0][1].text.replace(",", ""))
    losses = games - wins
    wr = floor((wins / games) * 100)

    # Update the dictionary.
    built_dict["overall_stats"]["games"] = games
    built_dict["overall_stats"]["losses"] = losses
    built_dict["overall_stats"]["wins"] = wins
    built_dict["overall_stats"]["win_rate"] = wr
    built_dict["overall_stats"]["rank"] = None  # We don't have a rank in Blizz data.

    # Build a dict using the stats.
    _a_s = {}
    _t_d = {}
    for subbox in stat_groups:
        trs = subbox.findall(".//tbody/tr")
        # Update the dict with [0]: [1]
        for subval in trs:
            name, value = subval[0].text.lower().replace(" ", "_").replace("_-_", "_"), subval[1].text
            nvl = util.try_extract(value)
            if 'average' in name.lower():
                _a_s[name.replace("_average", "")] = nvl
            else:
                _t_d[name] = nvl

    # Manually add the KPD.
    _t_d["kpd"] = round(_t_d["eliminations"] / _t_d["deaths"], 2)

    built_dict["game_stats"] = _t_d

    astats = []
    for astat in _a_s:
        if _t_d[astat] is not None:
            astats.append({"name": astat.replace("_", " "), "avg": _a_s[astat], "value": _t_d[astat]})

    built_dict["featured_stats"] = astats

    return built_dict


@bp.route("/v2/u/(.*)/stats/general")
@util.jsonify
async def bl_get_stats(ctx: HTTPRequestContext, battletag: str):
    """
    Get stats for a user using the Blizzard sources.
    """
    data = await bz.region_helper(ctx, battletag, region=ctx.request.values.get("region", None))
    if data == (None, None):
        raise HTTPException(404)

    parsed, region = data

    # Start the dict.
    built_dict = {"region": region, "battletag": battletag, "game_stats": [], "overall_stats": {}, "featured_stats": []}

    # Get the prestige.
    prestige = parsed.xpath(".//div[@class='player-level']")[0]
    # Extract the background-image from the styles.
    try:
        bg_image = [x for x in prestige.values() if 'background-image' in x][0]
    except IndexError:
        # Cannot find background-image.
        # Yikes!
        # Don't set a prestige.
        built_dict["overall_stats"]["prestige"] = 0
    else:
        for key, val in PRESTIGE.items():
            if key in bg_image:
                prestige_num = val
                break
        else:
            # Unknown.
            prestige_num = None
        built_dict["overall_stats"]["prestige"] = prestige_num

    # Parse out the HTML.
    level = int(parsed.findall(".//div[@class='player-level']/div")[0].text)
    built_dict["overall_stats"]["level"] = level

    hasrank = parsed.findall(".//div[@class='competitive-rank']/div")
    if hasrank:
        comprank = int(hasrank[0].text)
    else:
        comprank = None
    built_dict["overall_stats"]["comprank"] = comprank

    stat_groups = parsed.xpath(".//div[@data-group-id='stats' and @data-category-id='0x02E00000FFFFFFFF']")[0]
    # Highlight specific stat groups.
    death_box = stat_groups[4]
    game_box = stat_groups[6]

    # Calculate the wins, losses, and win rate.
    wins = int(game_box.xpath(".//text()[. = 'Games Won']/../..")[0][1].text.replace(",", ""))
    g = game_box.xpath(".//text()[. = 'Games Played']/../..")
    games = int(g[0][1].text.replace(",", ""))
    losses = games - wins
    wr = floor((wins / games) * 100)

    # Update the dictionary.
    built_dict["overall_stats"]["games"] = games
    built_dict["overall_stats"]["losses"] = losses
    built_dict["overall_stats"]["wins"] = wins
    built_dict["overall_stats"]["win_rate"] = wr
    built_dict["overall_stats"]["rank"] = None  # We don't have a rank in Blizz data.

    # Build a dict using the stats.
    _t_d = {}
    _a_s = {}
    for subbox in stat_groups:
        trs = subbox.findall(".//tbody/tr")
        # Update the dict with [0]: [1]
        for subval in trs:
            name, value = subval[0].text.lower().replace(" ", "_").replace("_-_", "_"), subval[1].text
            # Try and parse out the value. It might be a time!
            # If so, try and extract the time.
            nvl = util.try_extract(value)
            if 'average' in name.lower():
                _a_s[name.replace("_average", "")] = nvl
            else:
                _t_d[name] = nvl

    # Manually add the KPD.
    _t_d["kpd"] = round(_t_d["eliminations"] / _t_d["deaths"], 2)

    built_dict["game_stats"] = _t_d

    astats = []
    for astat in _a_s:
        if _t_d[astat] is not None:
            astats.append({"name": astat.replace("_", " "), "avg": _a_s[astat], "value": _t_d[astat]})

    built_dict["featured_stats"] = astats

    return built_dict


@bp.route("/v2/u/(.*)/stats")
@util.jsonify
async def redir_stats(ctx: HTTPRequestContext, battletag: str):
    built = "/api/v2/u/{}/stats/general".format(battletag)
    return {"error": 301, "loc": built}, 301, {"Location": built}


@bp.route("/v2/u/(.*)/heroes/(.*)")
@util.jsonify
async def get_extended_data(ctx: HTTPRequestContext, battletag: str, hero_name: str):
    """
    Gets extended information about a hero on a player.
    """

    hero_data_div_ids = {
        "reaper": "0x02E0000000000002",
        "tracer": "0x02E0000000000003",
        "mercy": "0x02E0000000000004",
        "hanzo": "0x02E0000000000005",
        "torbjorn": "0x02E0000000000006",
        "reinhardt": "0x02E0000000000007",
        "pharah": "0x02E0000000000008",
        "winston": "0x02E0000000000009",
        "widowmaker": "0x02E000000000000A",
        "bastion": "0x02E0000000000015",
        "symmetra": "0x02E0000000000016",
        "zenyatta": "0x02E0000000000020",
        "genji": "0x02E0000000000029",
        "roadhog": "0x02E0000000000040",
        "mccree": "0x02E0000000000042",
        "junkrat": "0x02E0000000000065",
        "zarya": "0x02E0000000000068",
        "s76": "0x02E000000000006E",
        "soldier76": "0x02E000000000006E",
        "lucio": "0x02E0000000000079",
        "d.va": "0x02E000000000007A",
        "dva": "0x02E000000000007A",
        "mei": "0x02E00000000000DD"
    }

    if not hero_name:
        return {
                   "error": 400,
                   "msg": "missing hero name"
               }, 400

    if hero_name in hero_data_div_ids:
        requested_hero_div_id = hero_data_div_ids[hero_name]
    else:
        return {
                   "error": 404,
                   "msg": "bad hero name"
               }, 404

    data = await bz.region_helper(ctx, battletag)

    if data == (None, None):
        raise HTTPException(404)

    parsed, region = data

    # Start the dict.
    built_dict = {"region": region, "battletag": battletag}

    stat_groups = parsed.xpath(
        ".//div[@data-group-id='stats' and @data-category-id='{0}']".format(requested_hero_div_id)
    )[0]

    _t_d = {}
    hero_specific_box = stat_groups[0]
    trs = hero_specific_box.findall(".//tbody/tr")
    # Update the dict with [0]: [1]
    for subval in trs:
        name, value = subval[0].text, subval[1].text
        if 'average' in name.lower():
            # No averages, ty
            continue
        nvl = util.try_extract(value)
        _t_d[name.lower().replace(" ", "_").replace("_-_", "_")] = nvl

    built_dict["hero_stats"] = _t_d

    _t_d = {}
    for subbox in stat_groups[1:]:
        trs = subbox.findall(".//tbody/tr")
        # Update the dict with [0]: [1]
        for subval in trs:
            name, value = subval[0].text, subval[1].text
            if 'average' in name.lower():
                # No averages, ty
                continue
            nvl = util.int_or_string(value)
            _t_d[name.lower().replace(" ", "_").replace("_-_", "_")] = nvl

    built_dict["general_stats"] = _t_d

    return built_dict


@bp.route("/v1/u/(.*)/stats")
@util.jsonify
async def get_stats(ctx: HTTPRequestContext, battletag: str):
    """
    Gets the stats for a user.
    """
    data = await mo.region_helper(ctx, battletag, region=ctx.request.values.get("region", None))
    if data == (None, None):
        raise HTTPException(404)

    parsed, region = data

    # Start the dict.
    built_dict = {"region": region, "battletag": battletag, "game_stats": [], "overall_stats": {}}

    kills = 0
    # Parse out the HTML.

    # Load the level.
    level = int(parsed.findall(".//div[@class='header-avatar']/span")[0].text)
    built_dict["overall_stats"]["level"] = level

    stats = parsed.xpath(".//div[contains(@class, 'stats-list-box')]")

    for child in stats:
        title, avg, count = child[::-1]

        # Unfuck numbers
        count = int(count.text.replace(",", ""))
        avg = float(avg.text.replace(" AVG", "").replace(",", ""))

        if title.text == "Eliminations":
            # Set kills.
            kills = int(count)
        elif title.text == "Deaths":
            # Add the KDA.
            try:
                built_dict["game_stats"].append({"name": "kpd", "avg": None, "value": kills / int(count)})
            except ZeroDivisionError:
                built_dict["game_stats"].append({"name": "kpd", "avg": None, "value": float("inf")})

        # Add it to the dict.
        built_dict["game_stats"].append({"name": title.text.lower(), "avg": avg, "value": int(count)})

    # Load up overall stats.
    ov_stats = parsed.findall(".//div[@class='header-stat']/strong")
    wins, losses = map(int, ov_stats[-2].text.replace(" ", "").replace("\t", "").split("/"))

    built_dict["overall_stats"]["wins"] = wins
    built_dict["overall_stats"]["losses"] = losses
    # The less things we have to scrape, the better.
    built_dict["overall_stats"]["games"] = wins + losses
    built_dict["overall_stats"]["winrate"] = round(wins / (wins + losses) * 100, 2)

    return built_dict


@bp.route("/v2/u/(.*)/heroes")
@util.jsonify
async def get_heroes(ctx: HTTPRequestContext, battletag: str):
    """
    Returns the top 5 heroes for the battletag specified.
    """


@bp.route("/v1/u/(.*)/heroes")
@util.jsonify
async def mo_get_heroes(ctx: HTTPRequestContext, battletag: str):
    """
    Returns the top 5 heroes for the battletag specified.
    """
    data = await mo.region_helper(ctx, battletag, region=ctx.request.values.get("region", None), extra="/heroes")
    if data == (None, None):
        raise HTTPException(404)

    parsed, region = data

    # Start the dict.
    built_dict = {"region": region, "battletag": battletag, "heroes": []}

    # Get the hero data and deconstruct it.
    hero_info = parsed.findall(".//div[@class='heroes-list']")[0]
    # Get the time info, and zip it together with the hero_info.
    times = parsed.findall(".//div[@class='heroes-stats-time']")
    for child, time in zip(hero_info, times):
        assert isinstance(child, etree._Element)
        # Don't check `heroes-columns`.
        kls = child.values()
        if any('heroes-columns' in x for x in kls):
            continue
        # The `see more` tag at the bottom.
        if child.tag != "div":
            continue

        # Parse the time into hours.
        hours = util.parse_time(time.text)

        # Split out the last part of the `data-href` so we can provide a link to extended hero data.
        url = child.xpath(".//a[@class='heroes-row-link']")[0].values()[1]
        id = int(url.split("/")[-1])

        built_url = "/api/v1/u/{}/heroes/{}".format(battletag, id)

        # Load the hero name.
        name = child.xpath(".//div[contains(@class, 'heroes-icon')]/strong/span")[0].text.lower()
        # Load the stats KPD.
        kpd = float(child.xpath(".//div[contains(@class, 'heroes-stats-kda')]/strong")[0].text)
        # Load the winrate.
        win_stats = child.xpath(".//span[contains(@class, 'heroes-stats-winrate')]/..")[0]
        # Get the win rate and the games played.
        winrate_raw = win_stats.xpath(".//span[@data-column = 'winrate']")[0].text
        winrate = float(winrate_raw[:-1])

        wins = win_stats.xpath(".//small[@class='bar-left']")[0].text[:-1]
        losses = win_stats.xpath(".//small[@class='bar-right']")[0].text[:-1]
        wins, losses = int(wins), int(losses)
        games = wins + losses

        # Create the dict.
        built_dict["heroes"].append({"name": name, "kpd": kpd, "winrate": winrate, "games": games,
                                     "extended_url": built_url, "hours": hours, "wins": wins, "losses": losses})

    return built_dict
