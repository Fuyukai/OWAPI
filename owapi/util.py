"""
Useful utilities.
"""
import json

from kyokai import Request
from kyokai.context import HTTPRequestContext


def jsonify(func):
    """
    JSON-ify the response from a function.
    """
    async def res(ctx: HTTPRequestContext):
        result = await func(ctx)
        assert isinstance(ctx.request, Request)
        if isinstance(result, tuple):
            new_result = {**{"_request": {"route": ctx.request.path, "api_ver": 1}},
                          **result[0]}
            if len(result) == 1:
                return json.dumps(new_result), 200, {"Content-Type": "application/json"}
            elif len(result) == 2:
                return json.dumps(new_result[0]), result[1], {"Content-Type": "application/json"}
            else:
                return json.dumps(new_result), result[1], {**{"Content-Type": "application/json"}, **result[2]}
        else:
            new_result = {**{"_request": {"route": ctx.request.path, "api_ver": 1}},
                          **result}
            return json.dumps(new_result), 200, {"Content-Type": "application/json"}

    return res
