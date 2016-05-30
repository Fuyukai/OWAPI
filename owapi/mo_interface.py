"""
This interfaces with MasterOverwatch to download stats.
"""
from kyokai.context import HTTPRequestContext
import aiohttp

# Constants.
from owapi import util

BASE_URL = "https://masteroverwatch.com/"
PROFILE_URL = BASE_URL + "profile/pc/"

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

