from kyokai.blueprints import Blueprint
from kyokai.context import HTTPRequestContext

from owapi import util

bp = Blueprint("routes", url_prefix="/api")


@bp.route("/")
@util.jsonify
async def root(ctx: HTTPRequestContext):
    """
    Return the root message.
    """
    return {}
