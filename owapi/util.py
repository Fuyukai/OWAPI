"""
Useful utilities.
"""
import json
import logging

import aioredis
from kyokai import Request
from kyokai.context import HTTPRequestContext

logger = logging.getLogger("OWAPI")


async def with_cache(ctx: HTTPRequestContext, func, *args, expires=300):
    """
    Run a coroutine with cache.

    Stores the result in redis.
    """
    assert isinstance(ctx.redis, aioredis.Redis)
    built = func.__name__ + repr(args)
    # Check for the key.
    # Uses a simple func name + repr(args) as the key to use.
    got = await ctx.redis.get(built)
    if got:
        logger.info("Cache hit for `{}`".format(built))
        if got == b"None":
            return None
        return got.decode()

    logger.info("Cache miss for `{}`".format(built))

    # Call the function.
    result = await func(ctx, *args)

    # Store the result as cached.
    if result is None:
        result = "None"
    await ctx.redis.set(built, result, expire=expires)
    return result


def jsonify(func):
    """
    JSON-ify the response from a function.
    """

    async def res(ctx: HTTPRequestContext, *args):
        result = await func(ctx, *args)
        assert isinstance(ctx.request, Request)
        if isinstance(result, tuple):
            new_result = {**{"_request": {"route": ctx.request.path, "api_ver": 1}},
                          **result[0]}
            if len(result) == 1:
                return json.dumps(new_result), 200, {"Content-Type": "application/json"}
            elif len(result) == 2:
                return json.dumps(new_result), result[1], {"Content-Type": "application/json"}
            else:
                return json.dumps(new_result), result[1], {**{"Content-Type": "application/json"}, **result[2]}
        else:
            if result:
                new_result = {**{"_request": {"route": ctx.request.path, "api_ver": 1}},
                              **result}
            else:
                new_result = {"_request": {"route": ctx.request.path, "api_ver": 1}}
            return json.dumps(new_result), 200, {"Content-Type": "application/json"}

    return res


def int_or_string(val: str):
    """
    Loads a value from MO into either an int or string value.

    String is returned if we can't turn it into an int.
    """
    new_s = val.replace(",", "")
    try:
        return float(new_s)
    except ValueError:
        return val


def parse_time(val: str) -> float:
    """
    Parse the time out into minutes.
    """
    unit = val.split(" ")[1]
    if 'minute' in unit:
        # Calculate the hour.
        mins = int(val.split(" ")[0])
        hours = round(mins/60, 3)
        return hours
    else:
        hours = val.split(" ")[0]
        return float(hours)
