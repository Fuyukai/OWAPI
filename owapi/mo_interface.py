"""
This interfaces with MasterOverwatch to download stats.
"""
import functools

import asyncio
import logging
import typing

from lxml import etree

from kyokai.context import HTTPRequestContext
import aiohttp

# Constants.
from owapi import util

BASE_URL = "https://masteroverwatch.com/"
PROFILE_URL = BASE_URL + "profile/pc/"
PAGE_URL = PROFILE_URL + "{region}/{btag}"

# This will break if Master Overwatch changes layout
# Make sure to change it if it does
heroes_xpath = "/html/body[@class='player']/main[@class='player-data']/div[@class='container']" \
               "/div[@class='row']/div[@class='col-md-4']/div[@class='data-heroes']/div[@class='heroes-list']"
stats_xpath = "/html/body[@class='player']/main[@class='player-data']/div[@class='container']/div[@class='row']" \
              "/div[@class='col-md-8']/div[@class='data-stats']/div[@class='stats-list']/div"

logger = logging.getLogger("OWAPI")

async def get_page_body(ctx: HTTPRequestContext, url: str) -> str:
    """
    Downloads page body from MasterOverwatch and caches it.
    """
    session = aiohttp.ClientSession(headers={"User-Agent": "OWAPI Scraper/1.0.0"})

    async def _real_get_body(_, url: str):
        # Real function.
        logger.info("GET => {}".format(url))
        async with session.get(url) as req:
            assert isinstance(req, aiohttp.ClientResponse)
            return await req.read()

    result = await util.with_cache(ctx, _real_get_body, url)
    session.close()
    return result


def _parse_page(content: str) -> etree._Element:
    """
    Internal function to parse a page and return the data.
    """
    data = etree.HTML(content)
    return data


async def get_user_page(ctx: HTTPRequestContext, battletag: str, region: str="eu", extra="") -> etree._Element:
    """
    Downloads the MO page for a user, and parses it.
    """
    built_url = PAGE_URL.format(region=region, btag=battletag.replace("#", "-")) + "{}".format(extra)
    page_body = await get_page_body(ctx, built_url)

    # parse the page
    parse_partial = functools.partial(_parse_page, page_body)
    loop = asyncio.get_event_loop()
    parsed = await loop.run_in_executor(None, parse_partial)

    return parsed


async def region_helper(ctx: HTTPRequestContext, battletag: str, region=None, extra=""):
    """
    Downloads the correct page for a user in the right region.

    This will return either (etree._Element, region) or (None, None).
    """
    result = (None, None)
    if region is None:
        for reg in ["eu", "us", "kr"]:
            page = await get_user_page(ctx, battletag, reg, extra)
            h_body = page.xpath("/html/body")[0].values()[0]
            # MO doesn't return a 404.
            # Instead, we check the body for an error class.
            # If it has it, just continue.
            if h_body == "error":
                continue
            else:
                # Return the parsed page, and the region.
                return page, reg
        else:
            # Since we continued without returning, give back the None, None.
            return result

    else:
        page = await get_user_page(ctx, battletag, region)
        h_body = page.xpath("/html/body")[0].values()[0]
        if h_body == "error":
            return result
        else:
            # Return the parsed page, and the region.
            return page, region