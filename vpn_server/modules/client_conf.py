import sys
import os
import subprocess

home_dir = "/home/wg-clients/"

# create home_dir if not exists
def initate():
    if os.path.exists(home_dir) == False:
        subprocess.check_output(["mkdir", home_dir])

def get_params():
    file = open('/etc/wireguard/params', 'r')
    raw_params = file.read().strip().split()
    file.close()
    
    params = dict()
    for p in raw_params:
        sz = len(p)
        key = ""
        value = ""
        for idx in range(0, sz):
            if p[idx] != '=':
                key += p[idx]
            else:
                value = p[idx + 1:]
                break
        params[key] = value
        
    return params

def client_exists(client_dir):
    return os.path.exists(client_dir)

def get_client_no():
    return len([x for x in os.listdir(home_dir) if os.path.isfile(os.path.join(home_dir, x))]) + 2

def add_client(client_id):
    try: 
        params = get_params()

        # create directory for the client
        initate()
        client_dir = home_dir + params['SERVER_WG_NIC'] + "-client-" + client_id
        if client_exists(client_dir) == True:
            return "VPN already provided"
        subprocess.check_output(["mkdir", client_dir])

        # generate public and private keys
        params['CLIENT_PRIV_KEY'] = subprocess.check_output(["wg", "genkey"])
        params['CLIENT_PUB_KEY'] = subprocess.check_output(["wg", "pubkey"], input = params['CLIENT_PRIV_KEY'])
        params['CLIENT_PRE_SHARED_KEY'] = subprocess.check_output(["wg", "genpsk"])

        params['CLIENT_PRIV_KEY'] = params['CLIENT_PRIV_KEY'].decode('utf-8')[:-1]
        params['CLIENT_PUB_KEY'] = params['CLIENT_PUB_KEY'].decode('utf-8')[:-1]
        params['CLIENT_PRE_SHARED_KEY'] = params['CLIENT_PRE_SHARED_KEY'].decode('utf-8')[:-1]

        # complete params
        params['ENDPOINT'] = params['SERVER_PUB_IP'] + ':' + params['SERVER_PORT']
        params['CLIENT_WG_IPV4'] = params['SERVER_WG_IPV4'][:-1] + str(get_client_no())

        # create the client file and add the server as a peer
        a = 'a' \
            'a' \
            
        client_file = '''[Interface]
            PrivateKey = ''' + params['CLIENT_PRIV_KEY'] + ''' 
            Address = ''' + params['CLIENT_WG_IPV4'] + '''/32
            DNS = ''' + params['CLIENT_DNS_1'] + ',' + params['CLIENT_DNS_2'] + '''

            [Peer]
            PublicKey = ''' + params['SERVER_PUB_KEY'] + '''
            PresharedKey = ''' + params['CLIENT_PRE_SHARED_KEY'] + '''
            Endpoint = ''' + params['ENDPOINT'] + '''
            AllowedIPs = 0.0.0.0/0,::/0'''

        file = open(client_dir + '/interface.conf', 'w')
        file.write(client_file)
        file.close()

        # add the client as a peer to the server
        peer_file = '''
    
### Client ''' + client_id + ''' 
[Peer]
PublicKey = ''' + params['CLIENT_PUB_KEY'] + '''
PresharedKey = ''' + params['CLIENT_PRE_SHARED_KEY'] + '''
AllowedIPs = ''' + params['CLIENT_WG_IPV4'] + '/32'

        file = open("/etc/wireguard/" + params['SERVER_WG_NIC'] + ".conf", "a")
        file.write(peer_file)
        file.close()

        subprocess.check_output(["systemctl", "restart", "wg-quick@" + params['SERVER_WG_NIC']])
        
        # generate qr code
        file = open(client_dir + "/interface.conf")
        subprocess.check_output(["qrencode", "-o", client_dir + "/qr.png"], stdin = file)
        file.close()

        return "OK"
    except subprocess.CalledProcessError as e:
        print(e.output)
        exit()

def revoke_client(client_id):
    try:
        params = get_params()

        # remove directory for the client
        client_dir = home_dir + params['SERVER_WG_NIC'] + "-client-" + client_id
        if client_exists(client_dir) == False:
            return "VPN already withholded"
        subprocess.check_output(["rm", "-rf", client_dir])

        # remove [Peer] block matching $client_id
        file = open("/etc/wireguard/" + params['SERVER_WG_NIC'] + ".conf", "r")
        lines = file.read().split('\n')
        file.close()

        new_file = ""
        sz = len(lines)
        i = 0
        while i < sz:
            if lines[i].strip() == "### Client " + client_id:
                i += 5
            else:
                new_file += lines[i] + "\n"
            i += 1

        file = open("/etc/wireguard/" + params['SERVER_WG_NIC'] + ".conf", "w")
        file.write(new_file)
        file.close()

        subprocess.check_output(["systemctl", "restart", "wg-quick@" + params['SERVER_WG_NIC']])

        return "OK"
    except subprocess.CalledProcessError as e:
        print(e.output)
        exit()
