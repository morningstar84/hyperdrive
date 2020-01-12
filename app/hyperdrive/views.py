from flask import jsonify, make_response

from app.model import Result
from app.network import HyperDrive
from . import hyperdrive


@hyperdrive.route('/')
def index(hyperdrive_network_service=HyperDrive.hyperdrive_network_service()):
    try:
        starship_list = hyperdrive_network_service.get_starship_list()
        subset_with_hyperdrive = list(filter(lambda x: x.has_hyperdrive_rating, starship_list))
        subset_with_no_hyperdrive = list(filter(lambda x: not x.has_hyperdrive_rating, starship_list))
        result = Result(subset_with_hyperdrive, subset_with_no_hyperdrive)
    except Exception as e:
        result = {
            "error": str(e)
        }
        return make_response(jsonify(result), 503)
    return jsonify(Result.to_dict(result))
