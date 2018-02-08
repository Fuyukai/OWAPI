"""
Main OWAPI App.
"""
import cProfile
import io
import json
import logging
import os
import pstats
import traceback

import aiohttp
from aiohttp import ClientSession
from asphalt.core import ContainerComponent
from kyoukai import Blueprint
from kyoukai import Kyoukai
from kyoukai.asphalt import KyoukaiComponent, HTTPRequestContext
from werkzeug.exceptions import HTTPException, InternalServerError
from werkzeug.routing import RequestRedirect
from werkzeug.wrappers import Response

from owapi.v3 import api_v3

# Fuck your logging config.

logging.basicConfig(filename='/dev/null', level=logging.INFO)

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(name)s -> %(message)s')
root = logging.getLogger()
root.handlers = []

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
root.addHandler(consoleHandler)

logger = logging.getLogger("OWAPI")


# Fucking aiohttp

class AiohttpHackyClientRequest(aiohttp.ClientRequest):
    def __init__(self, *args, **kwargs):
        kwargs["proxy_from_env"] = True
        super().__init__(*args, **kwargs)


# here's some more hotpatches, this api is a massive piece of garbage
async def handle_httpexception(self, ctx: HTTPRequestContext, exception: HTTPException,
                               environ: dict = None) -> Response:
    """
    Handle a HTTP Exception.

    :param ctx: The context of the request.
    :param exception: The HTTPException to handle.
    :param environ: The fake WSGI environment.

    :return: A :class:`werkzeug.wrappers.Response` that handles this response.
    """
    # Try and load the error handler recursively from the ctx.route.blueprint.
    bp = ctx.bp or self.root

    if environ is None:
        environ = ctx.environ

    cbl = lambda environ: Response("Internal server error during processing. Report this.",
                                   status=500)

    error_handler = bp.get_errorhandler(exception)
    if not error_handler:
        # Try the root Blueprint. This may happen if the blueprint requested isn't registered
        # properly in the root, for some reason.
        error_handler = self.root.get_errorhandler(exception)
        if not error_handler:
            # Just return the Exception's get_response.
            cbl = exception.get_response

    else:
        # Try and invoke the error handler to get the Response.
        # Wrap it in the try/except, so we can handle a default one.
        try:
            res = await error_handler.invoke(ctx, args=(exception,))
            # hacky way of unifying everything
            cbl = lambda environ: res
        except HTTPException as e:
            # why tho?
            logger.warning("Error handler function raised another error, using the "
                           "response from that...")
            cbl = e.get_response
        except Exception as e:
            logger.exception("Error in error handler!")
            cbl = InternalServerError(e).get_response
            # else:
            # result = wrap_response(result, self.response_class)

    try:
        result = cbl(environ=environ)
    except Exception:
        # ok
        logger.critical("Whilst handling a {}, response.get_response ({}) raised exception"
                        .format(exception.code, cbl), exc_info=True)
        result = Response("Critical server error. Your application is broken.",
                          status=500)

    if result.status_code != exception.code:
        logger.warning("Error handler {} returned code {} when exception was code {}..."
                       .format(error_handler.callable_repr, result.status_code,
                               exception.code))

    return result

Kyoukai.handle_httpexception = handle_httpexception


class APIComponent(ContainerComponent):
    """
    Container for other components. I think.
    """

    def __init__(self, components, use_redis=True, do_profiling=False, disable_ratelimits=False,
                 cache_time: int = None):
        super().__init__(components)
        app.config["owapi_use_redis"] = use_redis
        app.config["owapi_do_profiling"] = do_profiling
        app.config["owapi_disable_ratelimits"] = disable_ratelimits
        app.config["owapi_cache_time"] = cache_time

    async def start(self, ctx):
        self.add_component('kyoukai', KyoukaiComponent, ip="127.0.0.1", port=4444,
                           app="app:app", template_renderer=None)
        ctx.session = ClientSession(headers={"User-Agent": "owapi scraper/1.0.1"},
                                    request_class=AiohttpHackyClientRequest)
        if app.config["owapi_use_redis"]:
            from asphalt.redis.component import RedisComponent
            self.add_component('redis', RedisComponent)
        else:
            logger.warning('redis is disabled by config, rate limiting and caching not available')
        await super().start(ctx)

        logger.info("Started OWAPI server.")


app = Kyoukai("owapi")


@app.route("/")
async def root(ctx: HTTPRequestContext):
    raise RequestRedirect("https://github.com/SunDwarf/OWAPI/blob/master/api.md")


@app.root.errorhandler(500)
async def e500(ctx: HTTPRequestContext, exc: HTTPException):
    obb = {
        "error": 500,
        "msg": "please report this!",
        "exc": repr(exc.__cause__)
    }
    logger.error("Unhandled exception - Blizzard format probably changed!")
    traceback.print_exc()
    return json.dumps(obb), 500, {"Content-Type": "application/json"}


@app.root.errorhandler(404)
async def e404(ctx: HTTPRequestContext, exc: HTTPException):
    return json.dumps({"error": 404}), 404, {"Content-Type": "application/json"}


@app.root.before_request
async def start_profiling(ctx: HTTPRequestContext):
    if ctx.app.config["owapi_do_profiling"]:
        pr = cProfile.Profile()
        ctx.app.config['owapi_profiling_obj'] = pr
        pr.enable()
    return ctx


@app.root.after_request
async def stop_profiling(ctx: HTTPRequestContext, response: Response):
    if ctx.app.config["owapi_do_profiling"]:
        pr = ctx.app.config['owapi_profiling_obj']
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        # print into s, with regex filter
        ps.print_stats("owapi")
        # strip useless part of path infos and print with logger
        logger.info(s.getvalue().replace(
            os.path.split(os.path.dirname(os.path.realpath(__file__)))[0] + "/", ""
        ))
    return response


# Create the api blueprint and add children
api_bp = Blueprint("api", prefix="/api")


@api_bp.after_request
async def jsonify(ctx, response: Response):
    """
    JSONify the response.
    """
    if not isinstance(response.response, dict):
        return response

    # json.dump the body.
    status_code = response.status_code
    if not any(response.response.values()):
        status_code = 404
    if ctx.request.args.get("format", "json") in ["json_pretty", "pretty"]:
        d = json.dumps(response.response, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        d = json.dumps(response.response)
    response.set_data(d)
    response.headers["Content-Type"] = "application/json"
    response.status_code = status_code
    return response


api_bp.add_child(api_v3)

app.register_blueprint(api_bp)
