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
    built_dict = {"region": region, "battletag": battletag, "stats": []}

    stats = parsed.xpath(mo.stats_xpath)[0]

    kills = 0
    # Parse out the HTML.
    for child in stats.iterchildren():
        title, avg, count = child[::-1]

        # Unfuck numbers
        count = int(count.text.replace(",", ""))
        avg = float(avg.text.replace(" AVG", "").replace(",", ""))

        if title.text == "Eliminations":
            # Set kills.
            kills = int(count)
        elif title.text == "Deaths":
            # Add the KDA.
            built_dict["stats"].append({"name": "kpd", "avg": None, "value": kills / int(count)})

        # Add it to the dict.
        built_dict["stats"].append({"name": title.text.lower(), "avg": avg, "value": int(count)})

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
    for child in hero_info:
        assert isinstance(child, etree._Element)
        # The `see more` tag at the bottom.
        if child.tag != "div":
            continue

        # Load the hero name.
        name = child.xpath(".//div[contains(@class, 'heroes-icon')]/strong/span")[0].text
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
        built_dict["heroes"].append({"name": name, "kpd": kpd, "winrate": winrate, "games": games_played})

    return built_dict