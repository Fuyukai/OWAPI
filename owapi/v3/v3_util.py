"""
v3-specific utilities.
"""
import os

import shutil

import re

import functools
from ruamel import yaml
from kyoukai.asphalt import HTTPRequestContext

RATES_PATH = os.path.join(os.getcwd(), "rates.yml")

# No default user agents.
# Customize them, please.
DISALLOW_AGENTS = re.compile(r"(?:.*aiohttp/.*|.*python-requests/.*)")

# Bad useragent response text.
BAD_USERAGENT = {
                    "error": 400,
                    "msg": "Hi! To prevent abuse of this service, it is required that you customize your user agent."
                }, 400, {"Content-Type": "application/json"}

if not os.path.exists(RATES_PATH):
    shutil.copy(os.path.join(os.getcwd(), "rates.default.yml"), RATES_PATH)

with open(RATES_PATH) as r:
    ratelimits = yaml.load(r, Loader=yaml.Loader).get("rates")

compiled = []

# Compile the ratelimits.
for key, val in ratelimits.items():
    compiled.append((re.compile(key), val))

# Deref as we don't use it anymore
del ratelimits


def check_default_useragents(useragent: str):
    """
    Checks if the user agent matches a disallowed one.
    """
    return DISALLOW_AGENTS.match(useragent)


def with_ratelimit(bucket: str, timelimit: int=None, max_reqs: int=0):
    """
    Defines a function to rate limit for.

    Rate limits are stored in `rates.yml`.
    """

    # Compile regular expressions
    def _rl_inner1(func):
        @functools.wraps(func)
        async def _rl_inner2(ctx: HTTPRequestContext, *args, **kwargs):
            """
            Inner ratelimit function.
            """
            if ctx.app.config["owapi_disable_ratelimits"]:
                # Don't bother with ratelimits.
                return await func(ctx, *args, **kwargs)

            # only ratelimit if we have redis. Can't make this decision in
            # outer functions because they are called before globalsettings are set
            if ctx.app.config["owapi_use_redis"]:
                import aioredis
                assert isinstance(ctx.redis, aioredis.Redis)
                # Get the IP.
                ip = ctx.request.headers.get("X-Real-IP") or \
                    ctx.request.headers.get("X-Forwarded-For") or ctx.request.remote_addr

                # Build the ratelimit string.
                built = "{bucket}:{ip}:ratelimit".format(bucket=bucket, ip=ip)

                # Check the user agent before.
                user_agent = ctx.request.headers.get("User-Agent")

                if user_agent is None:
                    return BAD_USERAGENT

                if check_default_useragents(user_agent):
                    return BAD_USERAGENT

                # Load the rate limit based on the regular expression provided.
                for regex, rates in compiled:
                    if regex.match(user_agent):
                        break
                else:
                    # UH OH
                    raise RuntimeError("Failed to match User-Agent - did you wipe rates.yml?")

                _timelimit = timelimit or rates.get("time", 1)
                _max_reqs = max_reqs or rates.get("max_reqs", 1)

                # Redis-based ratelimiting.
                # First, check if the key even exists.
                if not (await ctx.redis.exists(built)):
                    # LPUSH, and EXPIRE it.
                    await ctx.redis.lpush(built, _max_reqs)
                    await ctx.redis.expire(built, _timelimit)
                else:
                    # LLEN it.
                    tries = await ctx.redis.llen(built)
                    if tries >= max_reqs:
                        # 429 You Are Being Ratelimited.
                        ttl = await ctx.redis.ttl(built)

                        if ttl == -1:
                            # wtf
                            await ctx.redis.expire(built, _timelimit)
                            ttl = _timelimit

                        return {"error": 429, "msg": "you are being ratelimited",
                                "retry": ttl}, 429, {"Retry-After": ttl}

                    # LPUSH a `1` or something onto the edge of the list.
                    # The actual value doesn't matter.
                    await ctx.redis.lpush(built, 1)

            # Now, await the underlying function.
            return await func(ctx, *args, **kwargs)

        return _rl_inner2

    return _rl_inner1
