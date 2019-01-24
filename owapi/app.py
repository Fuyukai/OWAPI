import json

import asks
import multio
import trio
from asks.response_objects import Response as ar
from html5_parser import parse
from quart import request
from quart_trio import QuartTrio

from owapi import parsing

multio.init("trio")

app = QuartTrio(__name__)

B_BASE_URL = "https://playoverwatch.com/en-us/"
B_PAGE_URL = B_BASE_URL + "career/{platform}/{btag}"
B_HEROES_URL = B_BASE_URL + "heroes"
B_HERO_URL = B_HEROES_URL + "/{hero}"


class ProfileNotFound(Exception):
    pass


class StatusError(Exception):
    pass


async def get_user_page(tag: str, platform: str):
    """
    Downloads a user page and parses it with LXML.
    """
    built_url = B_PAGE_URL.format(btag=tag.replace("#", "-"), platform=platform)
    result: ar = await asks.get(built_url)

    if result.status_code != 200:
        raise StatusError(result.status_code)

    def _parse(content: str):
        res = parse(content)
        node = res.findall(".//section[@class='u-nav-offset']//h1[@class='u-align-center']")
        for nodes in node:
            if nodes.text.strip() == "Profile Not Found":
                raise ProfileNotFound()

        return res

    parsed = await trio.run_sync_in_worker_thread(_parse, result.content)
    return parsed


def jsonify(result: dict, code: int = 200):
    return json.dumps(result), code, {"Content-Type": "application/json"}


# noinspection PyCallingNonCallable
@app.route("/api/v4/u/<tag>/blob")
async def get_blob(tag: str):
    """
    Gets the blob of data for a specified user.
    """
    try:
        result = await get_user_page(tag, platform=request.args.get("platform", "pc"))
    except StatusError as e:
        return jsonify({"code": e.args[0]}, e.args[0])

    status = result.xpath(".//p[@class='masthead-permission-level-text']")[0].text
    if status == "Private Profile":
        return jsonify({"error": "Private"}, 403)

    # noinspection PyDictCreation
    d = {
        "heroes": {
            "playtime": {
                "competitive": {},
                "quickplay": {}
            },
            "stats": {
                "competitive": {}, "quickplay": {}
            }
        },
        "stats": {},
        "achievements": {}
    }

    d["stats"]["quickplay"] = parsing.bl_parse_stats(result, status=status)
    d["stats"]["competitive"] = parsing.bl_parse_stats(result, mode="competitive",
                                                       status=status)

    d["heroes"]["stats"]["quickplay"] = parsing.bl_parse_hero_data(result)
    d["heroes"]["playtime"]["quickplay"] = parsing.bl_parse_all_heroes(result)

    d["heroes"]["stats"]["competitive"] = parsing.bl_parse_hero_data(result, mode="competitive")
    d["heroes"]["playtime"]["competitive"] = parsing.bl_parse_all_heroes(result,
                                                                         mode="competitive")

    d["achievements"] = parsing.bl_parse_achievement_data(result)

    return jsonify(d, 200)


if __name__ == "__main__":
    app.run()
