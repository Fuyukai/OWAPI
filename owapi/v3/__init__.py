"""
api_v3 routes.
"""
from kyoukai import HTTPRequestContext
from kyoukai import Response
from kyoukai.blueprints import Blueprint

from owapi.blizz_interface import fetch_all_user_pages
from owapi.v3.v3_util import with_ratelimit
from owapi.v3 import parsing

api_v3 = Blueprint("api_v3", url_prefix="/v3", reverse_hooks=True)


@api_v3.after_request
async def add__request(ctx: HTTPRequestContext, r: Response):
    # Edit the body, and add a _request.
    if isinstance(r.body, dict):
        # Add a _request var to the body.
        r.body["_request"] = {
            "api_ver": 3,
            "route": ctx.request.path
        }

    return r


@api_v3.route("/u/(.*)/blob")
@with_ratelimit("blob", timelimit=5, max_reqs=1)
async def get_blob(ctx: HTTPRequestContext, battletag: str):
    """
    Returns a giant blob of data.
    """
    pages = await fetch_all_user_pages(ctx, battletag, platform=ctx.request.args.get("platform"))

    built_dict = {}
    for region, result in pages.items():
        if result is None:
            built_dict[region] = None
            continue
        d = {
            "heroes": {"playtime": {"competitive": {}, "quickplay": {}}, "stats": {"competitive": {}, "quickplay": {}}},
            "stats": {}
        }

        d["stats"]["quickplay"] = parsing.bl_parse_stats(result)
        d["stats"]["competitive"] = parsing.bl_parse_stats(result, mode="competitive")

        d["heroes"]["stats"]["quickplay"] = parsing.bl_parse_hero_data(result)
        d["heroes"]["playtime"]["quickplay"] = parsing.bl_parse_all_heroes(result)

        d["heroes"]["stats"]["competitive"] = parsing.bl_parse_hero_data(result, mode="competitive")
        d["heroes"]["playtime"]["competitive"] = parsing.bl_parse_all_heroes(result, mode="competitive")

        built_dict[region] = d

    return built_dict

get_blob.should_convert = False


@api_v3.route("/u/(.*)/stats")
@with_ratelimit("stats")
async def get_stats(ctx: HTTPRequestContext, battletag: str):
    """
    Fetches stats about the user.
    """
    pages = await fetch_all_user_pages(ctx, battletag, platform=ctx.request.args.get("platform"))

    built_dict = {}
    for region, result in pages.items():
        if result is None:
            built_dict[region] = None
            continue
        d = {
            "heroes": {"playtime": {"competitive": {}, "quickplay": {}}, "stats": {"competitive": {}, "quickplay": {}}},
            "stats": {}
        }

        d["stats"]["quickplay"] = parsing.bl_parse_stats(result)
        d["stats"]["competitive"] = parsing.bl_parse_stats(result, mode="competitive")

        built_dict[region] = d

    return built_dict


get_stats.should_convert = False


@api_v3.route("/u/(.*)/heroes")
@with_ratelimit("stats")
async def get_heroes(ctx: HTTPRequestContext, battletag: str):
    """
    Fetches hero stats, in one big blob.
    """
    pages = await fetch_all_user_pages(ctx, battletag, platform=ctx.request.args.get("platform"))

    built_dict = {}
    for region, result in pages.items():
        if result is None:
            built_dict[region] = None
            continue
        d = {
            "heroes": {"playtime": {"competitive": {}, "quickplay": {}}, "stats": {"competitive": {}, "quickplay": {}}},
            "stats": {}
        }

        d["heroes"]["stats"]["quickplay"] = parsing.bl_parse_hero_data(result)
        d["heroes"]["playtime"]["quickplay"] = parsing.bl_parse_all_heroes(result)

        d["heroes"]["stats"]["competitive"] = parsing.bl_parse_hero_data(result, mode="competitive")
        d["heroes"]["playtime"]["competitive"] = parsing.bl_parse_all_heroes(result, mode="competitive")

        built_dict[region] = d

    return built_dict


# Separate routes.
@api_v3.route("/u/(.*)/heroes/quickplay")
@with_ratelimit("stats")
async def get_heroes_qp(ctx: HTTPRequestContext, battletag: str):
    """
    Fetches hero stats, for quick-play.
    """
    pages = await fetch_all_user_pages(ctx, battletag, platform=ctx.request.args.get("platform"))

    built_dict = {}
    for region, result in pages.items():
        if result is None:
            built_dict[region] = None
            continue
        d = {
            "heroes": {"playtime": {"competitive": {}, "quickplay": {}}, "stats": {"competitive": {}, "quickplay": {}}},
            "stats": {}
        }

        d["heroes"]["stats"]["quickplay"] = parsing.bl_parse_hero_data(result)

        d["heroes"]["playtime"]["quickplay"] = parsing.bl_parse_all_heroes(result)

        built_dict[region] = d

    return built_dict


get_heroes_qp.should_convert = False


@api_v3.route("/u/(.*)/heroes/competitive")
@with_ratelimit("stats")
async def get_heroes_comp(ctx: HTTPRequestContext, battletag: str):
    """
    Fetches hero stats, for competitive.
    """
    pages = await fetch_all_user_pages(ctx, battletag, platform=ctx.request.args.get("platform"))

    built_dict = {}
    for region, result in pages.items():
        if result is None:
            built_dict[region] = None
            continue
        d = {
            "heroes": {"playtime": {"competitive": {}, "quickplay": {}}, "stats": {"competitive": {}, "quickplay": {}}},
            "stats": {}
        }

        d["heroes"]["stats"]["competitive"] = parsing.bl_parse_hero_data(result, mode="competitive")

        d["heroes"]["playtime"]["competitive"] = parsing.bl_parse_all_heroes(result, mode="competitive")

        built_dict[region] = d

    return built_dict


get_heroes_comp.should_convert = False
