from os import path
import base64

def get_interface_path(clinet_id):
    return "/home/wg-clients/wg0-client-" + clinet_id + "/interface.conf"

def get_qr_path(client_id):
    return "/home/wg-clients/wg0-client-" + client_id + "/qr.png"

def get_interface(clinet_id):
    if path.exists(get_interface_path(clinet_id)) == False:
        return 'error'

    file = open(get_interface_path(clinet_id), 'r')
    meessage = file.read()
    file.close()

    return meessage

def get_qr(client_id):
    if path.exists(get_qr_path(client_id)) == False:
        return 'error'

    file = open(get_qr_path(client_id), 'rb')
    message = base64.b64encode(file.read()).decode('utf-8')

    return message
