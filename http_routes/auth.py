import logging
import jwt
from functools import wraps
from datetime import date, datetime, timedelta
from database.models.client import Client
from flask import (Blueprint, g, request, session, jsonify)
from database.repository.client_dao import ClientDao

bp = Blueprint('auth', __name__)

@bp.route('/user/login', methods=['POST'])
def signup_post():
    #
    request_data = request.get_json()

    if request_data is None or 'mail' not in request_data:
        return 'The email address is required.', 422
    elif 'password' not in request_data:
        return 'The password is required.', 422

    email = request_data['mail']
    password = request_data['password']

    if email is None or email == '':
        return 'The email address is required.', 422
    elif password is None or password == '':
        return 'The password is required.', 422
    try:
        if ClientDao.verify_authentication(email, password):
            user = ClientDao.get_by_mail(email)
            token = jwt.encode({
                'public_id': user.id,
                'exp' : datetime.utcnow() + timedelta(minutes = 30)
            }, 'my secret key')
    
            return (jsonify({'token' : token.decode('UTF-8')}), 201)
        else:
            return 'Incorrect address or password', 403
    except Exception as ex:
        logging.error(str(ex))
        return 'Server internal error', 403

@bp.route('/user/register', methods=["POST"])
def register():
    request_data = request.get_json()

    if request_data is None or 'mail' not in request_data:
        return 'The email address is required.', 422
    elif 'password' not in request_data:
        return 'The password is required.', 422

    mail = request_data['mail']
    password = request_data['password']

    if mail is None or mail == '':
        return 'The email address is required.', 422
    elif password is None or password == '':
        return 'The password is required.', 422

    try:
        client = Client(mail, date.today())
        client.password = password
        ClientDao.save(client)
        client = ClientDao.get_by_mail(mail)
        token = jwt.encode({
                'public_id': client.id,
                'exp' : datetime.utcnow() + timedelta(minutes = 30)
            }, 'my secret key')
    
        return (jsonify({'token' : token.decode('UTF-8')}), 201)
    except Exception:
        return 'A client with this mail is already registered.', 403
    
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return 'Token is missing', 401
  
        try:
            data = jwt.decode(token, 'my secret key')
            print(data)
            current_user = ClientDao.get_by_id(data['public_id'])
        except Exception as ex:
            return 'Token is invalid', 401
        return  f(current_user, *args, **kwargs)
  
    return decorated

@bp.route('/main', methods=["GET"])
@token_required
def main(current_user):
    return f'Hello {current_user.mail}!', 200


