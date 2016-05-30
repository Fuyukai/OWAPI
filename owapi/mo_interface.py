"""
This interfaces with MasterOverwatch to download stats.
"""
import functools

import asyncio
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

session = aiohttp.ClientSession(headers={"User-Agent": "OWAPI Scraper/1.0.0"})


async def get_page_body(ctx: HTTPRequestContext, url: str) -> str:
    """
    Downloads page body from MasterOverwatch and caches it.
    """

    async def _real_get_body(url: str):
        # Real function.
        async with session.get(url) as req:
            assert isinstance(req, aiohttp.ClientResponse)
            return await req.read()

    return await util.with_cache(ctx, _real_get_body, url)


def _parse_page(content: str) -> etree._Element:
    """
    Internal function to parse a page and return the data.
    """
    data = etree.HTML(content)
    return data


async def get_user_page(ctx: HTTPRequestContext, battletag: str, region: str="eu") -> etree._Element:
    """
    Downloads the MO page for a user, and parses it.
    """
    built_url = PAGE_URL.format(region, battletag.replace("#", "-"))
    page_body = await get_page_body(ctx, built_url)

    # parse the page
    parse_partial = functools.partial(_parse_page, page_body)
    loop = asyncio.get_event_loop()
    parsed = await loop.run_in_executor(None, parse_partial)

    return parsed

