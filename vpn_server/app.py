from flask import Flask, Response, request, send_file
import requests
import argparse
import jwt

from modules import client_conf, mail

app = Flask(__name__)

global my_token
my_token = None

def verify_access(token):
    global my_token
    if my_token:
        return token == my_token
    return False

@app.route('/add_client/<client_id>', methods = ['POST'])
def create_client(client_id):
    token = request.headers.get('Authorization')

    if verify_access(token) == False:
        return 'Access denied!', 400

    status = client_conf.add_client(client_id)
    if status == "OK":
        return Response("success", status = 200, mimetype = 'application/json')
    return status, 501

@app.route('/revoke_client/<client_id>', methods = ['POST'])
def revoke_client(client_id):
    token = request.headers.get('Authorization')

    if verify_access(token) == False:
        return 'Access denied!', 400

    status = client_conf.revoke_client(client_id)
    if status == "OK":
        return Response("success", status = 200, mimetype = 'application/json')
    return status, 501

@app.route('/get_interface/<client_id>', methods = ['POST'])
def get_interface(client_id):
    token = request.headers.get('Authorization')

    if verify_access(token) == False:
        return 'Access denied!', 400

    ret_val = mail.get_interface(client_id)
    if ret_val == 'error':
        return 'Client does not exist', 502
    
    return Response(ret_val, status = 200, mimetype = 'application/json')


@app.route('/get_qr/<client_id>', methods=['POST'])
def get_qr(client_id):
    token = request.headers.get('Authorization')

    if verify_access(token) == False:
        return 'Access denied!', 400

    ret_val = mail.get_qr(client_id)
    if ret_val == 'error':
        return 'Client does not exist', 502

    return Response(ret_val, status = 200, mimetype = 'application/json')

@app.route('/')
def basic():
    return 'Hello world'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('host', type = str, help = "Host to run on")
    # parser.add_argument('port', type = str, help = "Port to run on")
    # parser.add_argument('token', type = str, help = "Secret token")

    # args = parser.parse_args()

    # my_token = args.token
    host = '0.0.0.0'
    port = '5000'
    app.run(host = host, port = port)
