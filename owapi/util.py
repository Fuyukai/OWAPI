"""
Useful utilities.
"""
import logging
import re

import unidecode

from kyoukai.asphalt import HTTPRequestContext

logger = logging.getLogger("OWAPI")

HOUR_REGEX = re.compile(r"([0-9]*) hours?")
MINUTE_REGEX = re.compile(r"([0-9]*) minutes?")
SECOND_REGEX = re.compile(r"([0-9]*\.?[0-9]*) seconds?")
PERCENT_REGEX = re.compile(r"([0-9]{1,3})\s?\%")


async def with_cache(ctx: HTTPRequestContext, func, *args, expires=300, cache_404=False):
    """
    Run a coroutine with cache.

    Stores the result in redis.

    Unless we don't have redis.
    """

    if not ctx.app.config["owapi_use_redis"]:
        # no caching without redis, just call the function
        logger.info("Loading `{}` with disabled cache".format(repr(args)))
        result = await func(ctx, *args)
        return result
    else:
        import aioredis
        assert isinstance(ctx.redis, aioredis.Redis)
        built = func.__name__ + repr(args)
        # Check for the key.
        # Uses a simple func name + repr(args) as the key to use.
        got = await ctx.redis.get(built)
        if got and got != "None":
            if await ctx.redis.ttl(built) == -1:
                await ctx.redis.expire(built, expires)

            logger.info("Cache hit for `{}`".format(built))
            return got.decode()

        logger.info("Cache miss for `{}`".format(built))

        # Call the function.
        result = await func(ctx, *args)
        if result is None and not cache_404:
            # return None, no caching for 404s.
            return None

        # Store the result as cached.
        to_set = result if result else "None"
        logger.info("Storing {} with expiration {}".format(built, expires))
        await ctx.redis.set(built, to_set, expire=expires)
        if to_set == "None":
            return None
        return result


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
        hours = round(mins / 60, 3)
        return hours
    else:
        hours = val.split(" ")[0]
        return float(hours)


def try_extract(value):
    """
    Attempt to extract a meaningful value from the time.
    """
    get_float = int_or_string(value)
    # If it's changed, return the new int value.
    if get_float != value:
        return get_float

    # Next, try and get a time out of it.
    matched = HOUR_REGEX.match(value)
    if matched:
        val = matched.groups()[0]
        val = float(val)
        return val

    matched = MINUTE_REGEX.match(value)
    if matched:
        val = matched.groups()[0]
        val = float(val)
        val /= 60
        return val

    matched = SECOND_REGEX.match(value)
    if matched:
        val = matched.groups()[0]
        val = float(val)
        val = (val / 60 / 60)

        return val

    matched = PERCENT_REGEX.match(value)
    if matched:
        val = matched.groups()[0]
        val = float(val)
        val = (val / 100)

        return val

    # Check if there's an ':' in it.
    if ':' in value:
        sp = value.split(':')
        # If it's only two, it's mm:ss.
        # Formula is (minutes + (seconds / 60)) / 60
        if len(sp) == 2:
            mins, seconds = map(int, sp)
            mins += seconds / 60
            hours = mins / 60
            return hours

        # If it's three, it's hh:mm:ss.
        # Formula is hours + ((minutes + (seconds / 60)) / 60).
        elif len(sp) == 3:
            hours, mins, seconds = map(int, sp)
            mins += (seconds / 60)
            hours += (mins / 60)
            return hours
    else:
        # Just return the value.
        return value


def sanitize_string(string):
    """
    Convert an arbitrary string into the format used for our json keys
    """
    space_converted = re.sub(r'[-\s]', '_', unidecode.unidecode(string).lower())
    removed_nonalphanumeric = re.sub(r'\W', '', space_converted)
    underscore_normalized = re.sub(r'_{2,}', '_', removed_nonalphanumeric)
    return underscore_normalized.replace("soldier_76", "soldier76")  # backwards compatability
