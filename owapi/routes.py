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


@bp.route("/stats/(.*)")
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
            built_dict["stats"].append({"name": "kpd", "avg": None, "value": kills/int(count)})

        # Add it to the dict.
        built_dict["stats"].append({"name": title.text.lower(), "avg": avg, "value": int(count)})

    return built_dict
