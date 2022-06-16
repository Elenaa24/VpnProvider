from __future__ import absolute_import, print_function
from distutils.log import debug
import logging

from flask import Flask

from database.db_engine import DatabaseEngine
from database.repository.client_dao import ClientDao
from database.repository.server_dao import ServerDao
from database.models.client import Client
from database.models.server import Server
from database.repository.vpn_dao import VpnDao
from database.models.vpn import Vpn
import http_routes.auth as auth
import http_routes.overview as overview
from service.service import Service

# logging.basicConfig(filename='server.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
#     level = logging.INFO, datefmt='%d-%b-%y %H:%M:%S')

app = None  # Flask app

def create_app(testing=False):
    """Creates Flask main application."""
    global app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'my secret key'
    if testing:
        app.config['TESTING'] = True

    if not testing:
        DatabaseEngine.create_tables()

    app.register_blueprint(auth.bp)
    app.register_blueprint(overview.bp)

    return app


if __name__ == '__main__':
    create_app()
    app.run()


    
       
