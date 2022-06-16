import base64
from datetime import datetime, timedelta

import random

import requests
from database.models.client import Client
from database.models.server import Server
from database.models.vpn import Vpn
from database.repository.client_dao import ClientDao
from database.repository.country_dao import CountryDao
import json
import enum

from database.repository.server_dao import ServerDao
from database.repository.vpn_dao import VpnDao
from utils.my_exception import ExceptionType, MyException

class Vpn_actions(enum.Enum):
    add_client = 1
    get_interface = 2
    revoke_client = 3
    get_qr = 4

class Service():
    
    @staticmethod
    def get_countries():
        countries = CountryDao.get_all()
        json_string = []
        for c in countries:
            aux = f'"id": {c.id} , "name": "{c.name}"'
            aux = '{' + aux + '}'
            python_obj = json.loads(aux)
            json_string.append(python_obj)
        return json_string
    
    @staticmethod
    def post_vpn(country:str, plan:str, subscribe: bool, user:Client):
        servers = ServerDao.get_servers_with_given_country(country)
        servers_available = []
        for s in servers:
            if VpnDao.get_current_vpn_by_server_and_client(s.id, user.id) == None:
                servers_available.append(s)
        if len(servers_available) == 0:
            raise MyException('No available servers', type=ExceptionType.SERVER_ERROR)

        server = random.choice(servers_available)
        today = datetime.date(datetime.now())
        if plan == 'Basic':
            expiration_date = datetime.now() + timedelta(days=30)
        elif plan == 'Premium':
            expiration_date = datetime.now() + timedelta(days=90)
        elif plan == 'Enterprise':
            expiration_date = datetime.now() + timedelta(days=630)
        else:
            raise MyException('Invalid plan', type=ExceptionType.INVALID_DATA)
        
        expiration_date = datetime.date(expiration_date)
        vpn = Vpn(today, expiration_date, user, server, subscribe)
        resp = Service.perform_request(user, server, Vpn_actions.add_client.name)
        if resp.status_code == 200:
            VpnDao.save(vpn)
        else:
            raise MyException(f'Something wrong with the vpn server {server}. The error:{resp.text}', \
                type=ExceptionType.VPN_SERVER_ERROR)
    
    @staticmethod
    def revoke_client(user_id:int, server_id:int, vpn_id:int):
        client = ClientDao.get_by_id(user_id)
        server = ServerDao.get_by_id(server_id)
        resp = Service.perform_request(client, server, Vpn_actions.revoke_client.name)
        if resp.status_code == 200:
            VpnDao.modify_running(vpn_id, False)
            return True
        else:
            raise MyException(f'Something wrong with the vpn server {server}. The error:{resp.text}', \
                type=ExceptionType.VPN_SERVER_ERROR)

        
    @staticmethod
    def perform_request(user:Client, server:Server, action):
        url = f'http://{server.ip}:{server.port}'
        print(url + '/' + str(action) + '/' + str(user.id))
        resp = requests.post(url + '/' + str(action) + '/' + str(user.id))
                            # headers = {'Authorization' : access_token})
        return resp

    @staticmethod
    def get_all_vpns_for_client(user:Client):
        vpn = VpnDao.get_all_vpns_for_client(user.id)
        json_string = []
        for v in vpn:
            if v.running == True:
                conf = Service.get_interface(user, v.server)
                conf = conf.replace('\n', '\\n')
                qr = Service.get_qr(user, v.server)
                qr = 'data:image/png;base64,' + qr
            else:
                conf = ''
                qr = ' '

            aux = f'"id": {v.id}, "conf": "{conf}" , "country": "{v.server.country.name}" , "running": "{v.running}" , "expiration": "{v.expiration_date}", "qr": "{str(qr)}"'
            aux = '{' + aux + '}'
            python_obj = json.loads(aux)
            json_string.append(python_obj)
        print(json_string)
        return json_string
    
    @staticmethod
    def get_qr(user:Client, server:Server):
        resp = Service.perform_request(user, server, Vpn_actions.get_qr.name)
        if resp.status_code == 200:
            return resp.text
        else:
            raise MyException(f'Something wrong with the vpn server {server}. The error:{resp.text}', \
                type=ExceptionType.VPN_SERVER_ERROR)
    
    @staticmethod
    def get_interface(user:Client, server:Server):
        resp = Service.perform_request(user, server, Vpn_actions.get_interface.name)
        if resp.status_code == 200:
            return resp.text
        else:
            raise MyException(f'Something wrong with the vpn server {server}. The error:{resp.text}', \
                type=ExceptionType.VPN_SERVER_ERROR)
