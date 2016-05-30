"""
Useful utilities.
"""
import json

from kyokai.context import HTTPRequestContext


def jsonifiy(func):
    """
    JSON-ify the response from a function.
    """
    async def res(ctx: HTTPRequestContext):
        result = await func(ctx)
        if isinstance(result, tuple):
            if len(result) == 1:
                return json.dumps(result[0]), 200, {"Content-Type": "application/json"}
            elif len(result) == 2:
                return json.dumps(result[0]), result[1], {"Content-Type": "application/json"}
            else:
                return json.dumps(result[0]), result[1], {**{"Content-Type": "application/json"}, **result[2]}
        else:
            return json.dumps(result), 200, {"Content-Type": "application/json"}

    return res
