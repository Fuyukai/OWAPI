import json
from math import floor
import logging

from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound

import unidecode
from kyoukai.blueprint import Blueprint
from kyoukai.asphalt import HTTPRequestContext
from owapi import util
from owapi import blizz_interface as bz
from owapi.prestige import PRESTIGE

api_v2 = Blueprint("api_v2", prefix="/v2")

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
    "mei": "0x02E00000000000DD",
    "ana": "0x02E000000000013B",
    "sombra": "0x02E000000000012E"
}


@api_v2.after_request
async def add__request(ctx: HTTPRequestContext, r: Response):
    # Edit the body, and add a _request.
    if isinstance(r.response, dict):
        # Add a _request var to the body.
        r.response["_request"] = {
            "api_ver": 2,
            "route": ctx.request.path
        }

    return r


@api_v2.errorhandler(404)
async def a404(ctx: HTTPRequestContext, exc: HTTPException):
    """
    Return a 404 message, probably because the battletag was not found.
    """
    assert isinstance(ctx.request, Request)
    region = ctx.request.args.get("region", None)
    return json.dumps({"error": 404, "msg": "profile not found", "region": region}), \
           404, \
           {"Retry-After": 5,
            "Content-Type": "application/json"}


@api_v2.route("/")
async def root(ctx: HTTPRequestContext):
    """
    Return the root message.
    """
    return {
        "message": "API v2 is deprecated! It is recommended to use API v3 instead."
    }


@api_v2.route("/u/<battletag>/stats/competitive")
async def bl_get_compstats(ctx: HTTPRequestContext, battletag: str):
    """
    Get stats for a user using the Blizzard sources.
    """
    built_dict = await bl_get_stats("competitive", ctx, battletag)
    return built_dict


@api_v2.route("/u/<battletag>/stats/general")
async def bl_get_general_stats(ctx: HTTPRequestContext, battletag: str):
    """
    Get stats for a user using the Blizzard sources.
    """
    built_dict = await bl_get_stats("quickplay", ctx, battletag)
    return built_dict


async def bl_get_stats(mode, ctx, battletag):
    data = await bz.region_helper_v2(ctx, battletag, region=ctx.request.args.get("region", None),
                                     platform=ctx.request.args.get("platform", "pc"))

    if data == (None, None):
        raise NotFound()

    parsed, region = data

    # Start the dict.
    built_dict = {"region": region, "battletag": battletag, "game_stats": [], "overall_stats": {}, "average_stats": []}

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

    # Fetch Avatar
    built_dict["overall_stats"]["avatar"] = parsed.find(".//img[@class='player-portrait']").attrib['src']

    if mode == "competitive":
        hascompstats = parsed.xpath(".//div[@data-group-id='stats' and @data-category-id='0x02E00000FFFFFFFF']")
        if len(hascompstats) != 2:
            return {"error": 404, "msg": "competitive stats not found", "region": region}, 404
        stat_groups = hascompstats[1]
    elif mode == "quickplay":
        stat_groups = parsed.xpath(".//div[@data-group-id='stats' and @data-category-id='0x02E00000FFFFFFFF']")[0]
    else:
        # how else to handle fallthrough case?
        stat_groups = parsed.xpath(".//div[@data-group-id='stats' and @data-category-id='0x02E00000FFFFFFFF']")[0]

    # Highlight specific stat groups.
    try:
        game_box = stat_groups[6]
    except IndexError:
        try:
            game_box = stat_groups[5]
        except IndexError:
            return built_dict

    # Calculate the wins, losses, and win rate.
    try:
        wins = int(game_box.xpath(".//text()[. = 'Games Won']/../..")[0][1].text.replace(",", ""))
    except IndexError:
        # weird edge case
        wins = 0
    g = game_box.xpath(".//text()[. = 'Games Played']/../..")
    if len(g) < 1:
        # Blizzard fucked up, temporary quick fix for #70
        # This is still temporary as of mid october.
        games, losses = 0, 0
    else:
        games = int(g[0][1].text.replace(",", ""))

    if mode == "competitive":
        try:
            misc_box = stat_groups[7]
            losses = int(misc_box.xpath(".//text()[. = 'Games Lost']/../..")[0][1].text.replace(",", ""))
            ties = int(misc_box.xpath(".//text()[. = 'Games Tied']/../..")[0][1].text.replace(",", ""))
        except IndexError:
            losses = games - wins
            ties = 0

        if games == 0 or ties == 0:
            wr = 0
        else:
            wr = floor((wins / (games - ties)) * 100)

        built_dict["overall_stats"]["ties"] = ties
        built_dict["overall_stats"]["games"] = games
        built_dict["overall_stats"]["losses"] = losses
        built_dict["overall_stats"]["win_rate"] = wr

    # Update the dictionary.
    built_dict["overall_stats"]["wins"] = wins

    # Build a dict using the stats.
    _t_d = {}
    _a_d = {}
    for subbox in stat_groups:
        trs = subbox.findall(".//tbody/tr")
        # Update the dict with [0]: [1]
        for subval in trs:
            name, value = subval[0].text.lower().replace(" ", "_").replace("_-_", "_"), subval[1].text
            # Try and parse out the value. It might be a time!
            # If so, try and extract the time.
            nvl = util.try_extract(value)
            if 'average' in name.lower():
                _a_d[name.replace("_average", "_avg")] = nvl
            else:
                _t_d[name] = nvl

    # Manually add the KPD.
    try:
        _t_d["kpd"] = round(_t_d["eliminations"] / _t_d["deaths"], 2)
    except KeyError:
        _t_d["kpd"] = 0.0

    built_dict["game_stats"] = _t_d
    built_dict["average_stats"] = _a_d
    built_dict["competitive"] = mode == "competitive"

    return built_dict


@api_v2.route("/u/<battletag>/stats")
async def redir_stats(ctx: HTTPRequestContext, battletag: str):
    built = "/api/v2/u/{}/stats/general".format(battletag)
    return {"error": 301, "loc": built}, 301, {"Location": built}


@api_v2.route("/u/<battletag>/heroes/competitive")
async def get_heroes_competitive(ctx: HTTPRequestContext, battletag: str):
    """
    Returns the top 5 heroes and playtime for the battletag specified, in Competitive.
    """

    built_dict = await get_heroes("competitive", ctx, battletag)
    return built_dict


@api_v2.route("/u/<battletag>/heroes/general")
async def get_heroes_general(ctx: HTTPRequestContext, battletag: str):
    """
    Returns the top 5 heroes and playtime for the battletag specified, in Quickplay.
    """

    built_dict = await get_heroes("quickplay", ctx, battletag)
    return built_dict


async def get_heroes(mode, ctx, battletag):
    data = await bz.region_helper_v2(ctx, battletag, region=ctx.request.args.get("region", None),
                                     platform=ctx.request.args.get("platform", "pc"))

    if data == (None, None):
        raise NotFound()

    parsed, region = data

    built_dict = {"region": region, "battletag": battletag, "heroes": {}}

    if mode == "competitive":
        _hero_info = parsed.findall(".//div[@id='competitive']/section/div/div[@data-group-id='comparisons']")[0]
    elif mode == "quickplay":
        _hero_info = parsed.findall(".//div[@data-group-id='comparisons']")[0]
    else:
        _hero_info = parsed.findall(".//div[@data-group-id='comparisons']")[0]

    hero_info = _hero_info.findall(".//div[@class='bar-text']")

    # Loop over each one, extracting the name and hours counted.
    for child in hero_info:
        name, played = child.getchildren()
        name, played = name.text.lower(), played.text.lower()

        name = unidecode.unidecode(name)
        name = name.replace(".", "").replace(": ", "")  # d.va and soldier: 76 special cases

        if played == "--":
            time = 0
        else:
            time = util.try_extract(played)
        built_dict["heroes"][name] = time

    return built_dict


async def _get_extended_data(ctx, battletag, hero_name, competitive=False):
    if not hero_name:
        return {
                   "error": 400,
                   "msg": "missing hero name"
               }, 400

    hero_name = unidecode.unidecode(hero_name)

    if hero_name in hero_data_div_ids:
        requested_hero_div_id = hero_data_div_ids[hero_name]
    else:
        return {
                   "error": 404,
                   "msg": "bad hero name"
               }, 404

    data = await bz.region_helper_v2(ctx, battletag, region=ctx.request.args.get("region", None),
                                     platform=ctx.request.args.get("platform", "pc"))

    if data == (None, None):
        raise HTTPException(404)

    parsed, region = data

    # Start the dict.
    built_dict = {"region": region, "battletag": battletag}

    _root = parsed.xpath(
        ".//div[@data-mode='{}']".format("competitive" if competitive else "quickplay")
    )[0]

    _stat_groups = _root.xpath(
        ".//div[@data-group-id='stats' and @data-category-id='{0}']".format(requested_hero_div_id)
    )
    if len(_stat_groups) == 0:
        # no hero data
        return {"error": 404,
                "msg": "hero data not found"}, 404

    stat_groups = _stat_groups[0]

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
    built_dict["competitive"] = competitive

    return built_dict


@api_v2.route("/u/<battletag>/heroes/<hero_name>/competitive")
async def get_extended_data_comp(ctx: HTTPRequestContext, battletag: str, hero_name: str):
    return await _get_extended_data(ctx, battletag, hero_name, competitive=True)


@api_v2.route("/u/<battletag>/heroes/<hero_name>/general")
async def get_extended_data(ctx: HTTPRequestContext, battletag: str, hero_name: str):
    """
    Gets extended information about a hero on a player.
    """
    return await _get_extended_data(ctx, battletag, hero_name, competitive=False)


@api_v2.route("/u/<_>/heroes/<__>")
async def redir_extended_data(ctx: HTTPRequestContext, _, __):
    built = "/api/v2/u/{}/heroes/{}/general".format(_, __)
    return {"error": 301, "loc": built}, 301, {"Location": built}


@api_v2.route("/u/<battletag>/heroes")
async def redir_heroes(ctx: HTTPRequestContext, battletag: str):
    built = "/api/v2/u/{}/heroes/general".format(battletag)
    return {"error": 301, "loc": built}, 301, {"Location": built}
