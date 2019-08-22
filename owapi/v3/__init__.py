"""
api_v3 routes.
"""
import json

from kyoukai import Blueprint
from kyoukai.asphalt import HTTPRequestContext
from werkzeug.wrappers import Response

from owapi.blizz_interface import fetch_all_user_pages
from owapi.blizz_interface import get_all_heroes
from owapi.blizz_interface import get_hero_data
from owapi.v3 import parsing
from owapi.v3.v3_util import with_ratelimit

api_v3 = Blueprint("api_v3", prefix="/v3")


@api_v3.after_request
async def add__request(ctx: HTTPRequestContext, r: Response):
    # Edit the body, and add a _request.
    if isinstance(r.response, list):
        h = r.response[0]
    else:
        h = r.response
    if isinstance(h, dict):
        # Add a _request var to the body.
        h["_request"] = {"api_ver": 3, "route": ctx.request.path}

    return r


@api_v3.errorhandler(404)
async def e404(ctx: HTTPRequestContext, exc):
    return (
        json.dumps({"error": 404, "msg": "profile not found"}),
        404,
        {"Retry-After": 300, "Content-Type": "application/json"},
    )


@api_v3.route("/u/<battletag>/blob", reverse_hooks=True)
@with_ratelimit("blob", timelimit=5, max_reqs=1)
async def get_blob(ctx: HTTPRequestContext, battletag: str):
    """
    Returns a giant blob of data.
    """
    pages = await fetch_all_user_pages(
        ctx, battletag, platform=ctx.request.args.get("platform", "pc")
    )

    built_dict = {}
    for region, result in pages.items():
        if result is None:
            built_dict[region] = None
            continue

        status = result.xpath(".//p[@class='masthead-permission-level-text']")[0].text
        if status == "Private Profile":
            return {"error": "Private"}, 403

        d = {
            "heroes": {
                "playtime": {"competitive": {}, "quickplay": {}},
                "stats": {"competitive": {}, "quickplay": {}},
            },
            "stats": {},
            "achievements": {},
        }

        d["stats"]["quickplay"] = parsing.bl_parse_stats(result, status=status)
        d["stats"]["competitive"] = parsing.bl_parse_stats(
            result, mode="competitive", status=status
        )

        d["heroes"]["stats"]["quickplay"] = parsing.bl_parse_hero_data(result)
        d["heroes"]["playtime"]["quickplay"] = parsing.bl_parse_all_heroes(result)

        d["heroes"]["stats"]["competitive"] = parsing.bl_parse_hero_data(result, mode="competitive")
        d["heroes"]["playtime"]["competitive"] = parsing.bl_parse_all_heroes(
            result, mode="competitive"
        )

        d["achievements"] = parsing.bl_parse_achievement_data(result)

        built_dict[region] = d

    return built_dict


@api_v3.route("/u/<battletag>/stats", reverse_hooks=True)
@with_ratelimit("stats")
async def get_stats(ctx: HTTPRequestContext, battletag: str):
    """
    Fetches stats about the user.
    """
    pages = await fetch_all_user_pages(
        ctx, battletag, platform=ctx.request.args.get("platform", "pc")
    )

    built_dict = {}
    for region, result in pages.items():
        if result is None:
            built_dict[region] = None
            continue

        status = result.xpath(".//p[@class='masthead-permission-level-text']")[0].text
        # if status == "Private Profile":
        #     return {"error": "Private"}, 403

        d = {"stats": {}}

        d["stats"]["quickplay"] = parsing.bl_parse_stats(result, status=status)
        d["stats"]["competitive"] = parsing.bl_parse_stats(
            result, mode="competitive", status=status
        )

        built_dict[region] = d

    return built_dict


@api_v3.route("/u/<battletag>/heroes", reverse_hooks=True)
@with_ratelimit("stats")
async def get_heroes(ctx: HTTPRequestContext, battletag: str):
    """
    Fetches hero stats, in one big blob.
    """
    pages = await fetch_all_user_pages(
        ctx, battletag, platform=ctx.request.args.get("platform", "pc")
    )

    built_dict = {}
    for region, result in pages.items():
        if result is None:
            built_dict[region] = None
            continue

        status = result.xpath(".//p[@class='masthead-permission-level-text']")[0].text
        if status == "Private Profile":
            return {"error": "Private"}, 403

        d = {
            "heroes": {
                "playtime": {"competitive": {}, "quickplay": {}},
                "stats": {"competitive": {}, "quickplay": {}},
            }
        }

        d["heroes"]["stats"]["quickplay"] = parsing.bl_parse_hero_data(result)
        d["heroes"]["playtime"]["quickplay"] = parsing.bl_parse_all_heroes(result)

        d["heroes"]["stats"]["competitive"] = parsing.bl_parse_hero_data(result, mode="competitive")
        d["heroes"]["playtime"]["competitive"] = parsing.bl_parse_all_heroes(
            result, mode="competitive"
        )

        built_dict[region] = d

    return built_dict


# Separate routes.
@api_v3.route("/u/<battletag>/heroes/quickplay", reverse_hooks=True)
@with_ratelimit("stats")
async def get_heroes_qp(ctx: HTTPRequestContext, battletag: str):
    """
    Fetches hero stats, for quick-play.
    """
    pages = await fetch_all_user_pages(
        ctx, battletag, platform=ctx.request.args.get("platform", "pc")
    )

    built_dict = {}
    for region, result in pages.items():
        if result is None:
            built_dict[region] = None
            continue

        status = result.xpath(".//p[@class='masthead-permission-level-text']")[0].text
        if status == "Private Profile":
            return {"error": "Private"}, 403

        d = {
            "heroes": {
                "playtime": {"competitive": {}, "quickplay": {}},
                "stats": {"competitive": {}, "quickplay": {}},
            }
        }

        d["heroes"]["stats"]["quickplay"] = parsing.bl_parse_hero_data(result)

        d["heroes"]["playtime"]["quickplay"] = parsing.bl_parse_all_heroes(result)

        built_dict[region] = d

    return built_dict


@api_v3.route("/u/<battletag>/heroes/competitive", reverse_hooks=True)
@with_ratelimit("stats")
async def get_heroes_comp(ctx: HTTPRequestContext, battletag: str):
    """
    Fetches hero stats, for competitive.
    """
    pages = await fetch_all_user_pages(
        ctx, battletag, platform=ctx.request.args.get("platform", "pc")
    )

    built_dict = {}
    for region, result in pages.items():
        if result is None:
            built_dict[region] = None
            continue

        status = result.xpath(".//p[@class='masthead-permission-level-text']")[0].text
        if status == "Private Profile":
            return {"error": "Private"}, 403

        d = {
            "heroes": {
                "playtime": {"competitive": {}, "quickplay": {}},
                "stats": {"competitive": {}, "quickplay": {}},
            }
        }

        d["heroes"]["stats"]["competitive"] = parsing.bl_parse_hero_data(result, mode="competitive")

        d["heroes"]["playtime"]["competitive"] = parsing.bl_parse_all_heroes(
            result, mode="competitive"
        )

        built_dict[region] = d

    return built_dict


@api_v3.route("/u/<battletag>/achievements", reverse_hooks=True)
@with_ratelimit("stats")
async def get_achievements(ctx: HTTPRequestContext, battletag: str):
    """
    Fetches hero stats, for competitive.
    """
    pages = await fetch_all_user_pages(
        ctx, battletag, platform=ctx.request.args.get("platform", "pc")
    )

    built_dict = {}
    for region, result in pages.items():
        if result is None:
            built_dict[region] = None
            continue

        status = result.xpath(".//p[@class='masthead-permission-level-text']")[0].text
        if status == "Private Profile":
            return {"error": "Private"}, 403

        d = {"achievements": parsing.bl_parse_achievement_data(result)}

        built_dict[region] = d

    return built_dict


@api_v3.route("/heroes", reverse_hooks=True)
async def get_hero_list(ctx: HTTPRequestContext):
    """
    Send hero list.
    """
    parsed = await get_all_heroes(ctx)
    heroes = parsing.bl_get_all_heroes(parsed)

    built_dict = {"Offense": {}, "Defense": {}, "Tank": {}, "Support": {}}
    for hero in heroes:
        _parsed = await get_hero_data(ctx, hero.lower())
        retHero = parsing.bl_find_heroes(_parsed)
        built_dict[retHero["role"]][hero] = retHero

    return built_dict


@api_v3.route("/heroes/<hero>", reverse_hooks=True)
async def get_hero(ctx: HTTPRequestContext, hero: str):
    """
    Send hero data for selected hero.
    """
    parsed = await get_hero_data(ctx, hero)
    _hero = parsing.bl_find_heroes(parsed)
    _hero["name"] = hero
    return _hero


get_achievements.should_convert = False
