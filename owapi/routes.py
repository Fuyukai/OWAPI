from lxml import etree

from kyokai import Request
from kyokai.blueprints import Blueprint
from kyokai.context import HTTPRequestContext
from kyokai.exc import HTTPException

from owapi import util
from owapi import mo_interface as mo

bp = Blueprint("routes", url_prefix="/api")


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


@bp.route("/u/(.*)/stats")
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
            built_dict["game_stats"].append({"name": "kpd", "avg": None, "value": kills / int(count)})

        # Add it to the dict.
        built_dict["game_stats"].append({"name": title.text.lower(), "avg": avg, "value": int(count)})

    # Load up overall stats.
    ov_stats = parsed.findall(".//div[@class='header-stat']/strong")
    # Don't even loop over these.
    built_dict["overall_stats"]["rank"] = int(ov_stats[0].text[1:].replace(",", ""))
    built_dict["overall_stats"]["games"] = int(ov_stats[1].text.replace(",", ""))
    built_dict["overall_stats"]["wins"] = int(ov_stats[2].text.split("/")[0])
    built_dict["overall_stats"]["losses"] = int(ov_stats[2].text.split("/")[1])
    built_dict["overall_stats"]["win_rate"] = float(ov_stats[3].text[:-1])

    return built_dict


@bp.route("/u/(.*)/heroes/([0-9]*)")
@util.jsonify
async def get_extended_data(ctx: HTTPRequestContext, battletag: str, hero_id: str):
    """
    Gets extended information about a hero on a player.
    """
    data = await mo.region_helper(ctx, battletag, region=ctx.request.values.get("region", None),
                                  extra="/heroes/" + hero_id)
    if data == (None, None):
        raise HTTPException(404)

    parsed, region = data

    # Start the dict.
    built_dict = {"region": region, "battletag": battletag, "stats": []}

    stats = parsed.findall(".//div[@class='hero-stats']")

    # Loop over each block of stats.
    for block in stats:
        title = block.findall(".//div[@class='stats-title']")[0].text.lower()
        stat_groups = block.findall(".//div[@class='stats-box']")

        l_stats = []
        # Loop over each stat group, and add it to l_stats.
        for stat in stat_groups:
            name = stat.xpath(".//span")[0].text.lower()
            count = util.int_or_string(stat.xpath(".//strong")[0].text)
            l_stats.append({"name": name, "value": count})

        built_dict["stats"].append({"name": title, "stats": l_stats})

    return built_dict


@bp.route("/u/(.*)/heroes")
@util.jsonify
async def get_heroes(ctx: HTTPRequestContext, battletag: str):
    """
    Returns the top 5 heroes for the battletag specified.
    """
    data = await mo.region_helper(ctx, battletag, region=ctx.request.values.get("region", None))
    if data == (None, None):
        raise HTTPException(404)

    parsed, region = data

    # Start the dict.
    built_dict = {"region": region, "battletag": battletag, "heroes": []}

    # Get the hero data and deconstruct it.
    hero_info = parsed.findall(".//div[@class='heroes-list']")[0]
    # Get the time info, and zip it together with the hero_info.
    times = parsed.findall(".//div[@class='heroes-details-title']/time")
    for child, time in zip(hero_info, times):
        assert isinstance(child, etree._Element)
        # The `see more` tag at the bottom.
        if child.tag != "div":
            continue

        # Parse the time into hours.
        hours = util.parse_time(time.text)

        # Split out the last part of the `data-href` so we can provide a link to extended hero data.
        url = child.values()[1]
        id = int(url.split("/")[-1])

        built_url = "/api/u/{}/heroes/{}".format(battletag, id)

        # Load the hero name.
        name = child.xpath(".//div[contains(@class, 'heroes-icon')]/strong/span")[0].text.lower()
        # Load the stats KPD.
        kpd = float(child.xpath(".//div[contains(@class, 'heroes-stats')]/div/strong")[0].text)
        # Load the winrate.
        win_stats = child.xpath(".//div[contains(@class, 'heroes-winrate')]")[0]
        # Get the win rate and the games played.
        winrate_raw = win_stats.xpath(".//strong")[0].text
        winrate = float(winrate_raw[:-1])
        games_played_raw = win_stats.xpath(".//span")[0].text
        games_played = int(games_played_raw.split(" ")[0])
        # Create the dict.
        built_dict["heroes"].append({"name": name, "kpd": kpd, "winrate": winrate, "games": games_played,
                                     "extended_url": built_url, "hours": hours})

    return built_dict
