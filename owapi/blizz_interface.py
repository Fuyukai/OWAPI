"""
Interface that uses Blizzard's pages as the source.
"""
import functools
import logging

import asyncio
import traceback

from lxml import etree

import aiohttp
from kyoukai.context import HTTPRequestContext

from owapi import util

B_BASE_URL = "https://playoverwatch.com/en-us/"
B_PAGE_URL = B_BASE_URL + "career/{platform}{region}/{btag}"

# The currently available specific regions.
AVAILABLE_REGIONS = ["/eu", "/us", "/kr"]

logger = logging.getLogger("OWAPI")


async def get_page_body(ctx: HTTPRequestContext, url: str, cache_time=300, cache_404=False) -> str:
    """
    Downloads page body from MasterOverwatch and caches it.
    """
    session = aiohttp.ClientSession(headers={"User-Agent": "OWAPI Scraper/1.0.1"})

    async def _real_get_body(_, url: str):
        # Real function.
        logger.info("GET => {}".format(url))
        async with session.get(url) as req:
            assert isinstance(req, aiohttp.ClientResponse)
            logger.info("GET => {} => {}".format(url, req.status))
            if req.status != 200:
                return None
            return (await req.read()).decode()

    result = await util.with_cache(ctx, _real_get_body, url, expires=cache_time, cache_404=cache_404)
    session.close()
    return result


def _parse_page(content: str) -> etree._Element:
    """
    Internal function to parse a page and return the data.
    """
    if content and content.lower() != 'none':
        data = etree.HTML(content)
        return data


async def get_user_page(ctx: HTTPRequestContext, battletag: str, platform: str = "pc", region: str = "us",
                        cache_time=300, cache_404=False) -> etree._Element:
    """
    Downloads the BZ page for a user, and parses it.
    """
    if platform != "pc":
        region = ""
    built_url = B_PAGE_URL.format(
        region=region, btag=battletag.replace("#", "-"), platform=platform)
    page_body = await get_page_body(ctx, built_url, cache_time=cache_time, cache_404=cache_404)

    if not page_body:
        return None

    # parse the page
    parse_partial = functools.partial(_parse_page, page_body)
    loop = asyncio.get_event_loop()
    parsed = await loop.run_in_executor(None, parse_partial)

    return parsed


async def fetch_all_user_pages(ctx: HTTPRequestContext, battletag: str, *,
                               platform="pc"):
    """
    Fetches all user pages for a specified user.

    Returns a dictionary in the format of `{region: etree._Element | None}`.
    """
    if platform != "pc":
        coro = get_user_page(ctx, battletag, region="", platform=platform, cache_404=True)
        result = await coro
        if isinstance(result, etree._Element):
            return {"all": result,
                    "eu": None, "us": None, "kr": None}
        else:
            return {"all": None,
                    "eu": None, "us": None, "kr": None}

    futures = []
    for region in AVAILABLE_REGIONS:
        # Add the get_user_page coroutine.
        coro = get_user_page(ctx, battletag, region=region, platform=platform, cache_404=True)
        futures.append(coro)

    # Gather all the futures to download paralellely.
    results = await asyncio.gather(*futures, return_exceptions=True)
    d = {}
    for region, result in zip(AVAILABLE_REGIONS, results):
        # Remove the `/` from the front of the region.
        # This is used internally to make building the URL to get simpler.
        region = region[1:]
        # Make sure it's either a None or an element.
        if isinstance(result, etree._Element):
            d[region] = result
        elif isinstance(result, Exception):
            logger.error("Failed to fetch user page!\n{}".format(
                traceback.format_exception(type(result), result, result.__traceback__)
            ))
            d[region] = None
        else:
            d[region] = None

    return d


async def region_helper_v2(ctx: HTTPRequestContext, battletag: str, platform="pc", region=None, extra=""):
    """
    Downloads the correct page for a user in the right region.

    This will return either (etree._Element, region) or (None, None).
    """
    if region is None:
        reg_l = ["/eu", "/us", "/kr"]
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
