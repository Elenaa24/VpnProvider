import traceback
import logging
from flask import Blueprint, jsonify, request
from database.models.client import Client
from database.repository.client_dao import ClientDao
from http_routes.auth import token_required

from service.service import Service

bp = Blueprint('overview', __name__)

@bp.route('/countries', methods=['GET'])
@token_required
def get_vpn_countries(user=None):
    # user = Client(1, 'idk', 'ida')
    try:
        country_list = Service.get_countries()
    except Exception as ex:
        logging.error(str(ex))
        print(ex)
        return 'Server internal error', 403
    return jsonify(country_list), 200

@bp.route('/vpn', methods=['POST'])
@token_required
def post_vpn(user):
    try:
        print(user)
        request_data = request.get_json()
        country = request_data['country']
        plan = request_data['plan']
        subscribe = request_data['subscribe']
        Service.post_vpn(country, plan, subscribe, user)
        return 'ok', 200

    except Exception as ex:
        logging.error(str(ex))
        traceback.print_exc()
        print(ex)
        return 'Server internal error', 403

@bp.route('/vpns', methods=['GET'])
@token_required
def get_vpns(user=None):
    # user = Client(1, 'idk', 'ida')
    try:
        res = Service.get_all_vpns_for_client(user)

    except Exception as ex:
        logging.error(str(ex))
        print(ex)
        return 'Server internal error', 403

    return jsonify(res), 200
