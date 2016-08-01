"""
Interface that uses Blizzard's pages as the source.
"""
import functools
import logging

import asyncio
from lxml import etree

import aiohttp
from kyoukai.context import HTTPRequestContext

from owapi import util

B_BASE_URL = "https://playoverwatch.com/en-us/"
B_PAGE_URL = B_BASE_URL + "career/{platform}{region}/{btag}"

logger = logging.getLogger("OWAPI")


async def get_page_body(ctx: HTTPRequestContext, url: str, cache_time=300) -> str:
    """
    Downloads page body from MasterOverwatch and caches it.
    """
    session = aiohttp.ClientSession(headers={"User-Agent": "OWAPI Scraper/1.0.0"})

    async def _real_get_body(_, url: str):
        # Real function.
        logger.info("GET => {}".format(url))
        async with session.get(url) as req:
            assert isinstance(req, aiohttp.ClientResponse)
            if req.status != 200:
                return None
            return (await req.read()).decode()

    result = await util.with_cache(ctx, _real_get_body, url, expires=cache_time)
    session.close()
    return result


def _parse_page(content: str) -> etree._Element:
    """
    Internal function to parse a page and return the data.
    """
    if content:
        data = etree.HTML(content)
        return data


async def get_user_page(ctx: HTTPRequestContext, battletag: str, platform: str="pc", region: str = "us", extra="",
                        cache_time=300) -> etree._Element:
    """
    Downloads the BZ page for a user, and parses it.
    """
    if platform != "pc":
        region = ""
    built_url = B_PAGE_URL.format(
        region=region, btag=battletag.replace("#", "-"), platform=platform) + "{}".format(extra)
    page_body = await get_page_body(ctx, built_url, cache_time=cache_time)

    if not page_body:
        return None

    # parse the page
    parse_partial = functools.partial(_parse_page, page_body)
    loop = asyncio.get_event_loop()
    parsed = await loop.run_in_executor(None, parse_partial)

    return parsed


async def region_helper(ctx: HTTPRequestContext, battletag: str, platform="pc", region=None, extra=""):
    """
    Downloads the correct page for a user in the right region.

    This will return either (etree._Element, region) or (None, None).
    """
    if region is None:
        reg_l = ["/eu", "/us", "/cn", "/kr"]
    else:
        if not region.startswith("/"):
            # ugh
            region = "/" + region
        reg_l = [region]

    for reg in reg_l:
        # Get the user page.
        page = await get_user_page(ctx, battletag, platform, reg, extra)
        # Check if the page was returned successfully.
        # If it was, return it.
        if page is not None:
            return page, reg[1:]
    else:
        # Since we continued without returning, give back the None, None.
        return None, None
