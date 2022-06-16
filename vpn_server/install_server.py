#! /usr/bin/env python
import os
import logging
import subprocess

logging.basicConfig(filename='install_wireguard.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
    level = logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
 
def verify_if_is_root():
    if not os.geteuid()==0:
        raise Exception('This script must be run as root!')

def install_wireguard():
    command1 = ['apt-get', 'update']
    command2 = ['apt-get', 'install', '-y', 'wireguard', 'iptables', 'resolvconf', 'qrencode']
    subprocess.check_call(command1)
    subprocess.check_call(command2)

def install_flask():
    # cmd = ['sudo', 'apt', 'install', 'python3-venv']
    # subprocess.check_call(cmd)
    # cmd = ['mkdir', '/etc/flask_dir']
    # subprocess.check_call(cmd)
    # cmd = ['python3', '-m', 'venv', 'venv']
    # subprocess.check_call(cmd, cwd='/etc/flask_dir')
    # cmd = ['source', 'venv/bin/activate']
    # subprocess.check_call(cmd, cwd='/etc/flask_dir')
    # cmd = ['echo', "'Y'", '|', 'apt', 'install', 'python3-flask']
    cmd = ["'yes' | apt install python3-flask"]
    print(cmd)
    subprocess.check_call(cmd, cwd='/etc/flask_dir', shell=True)

def set_app_to_at_restart():
    create_service_file_command = ['touch', '/lib/systemd/system/myservice.service']
    subprocess.call(create_service_file_command)
    with open('/lib/systemd/system/myservice.service', 'w') as file:
        contex = '''[Unit]
            Description=My Lovely Service
            After=network.target

            [Service]
            Type=idle
            Restart=on-failure
            User=root
            ExecStart=/bin/bash -c 'cd /home/vpn_server/ && python3 app.py'

            [Install]
            WantedBy=multi-user.target
            '''
        file.write(contex)
    set_permission_cmd = ['sudo', 'chmod', '644', '/lib/systemd/system/myservice.service']
    subprocess.check_call(set_permission_cmd)
    reload_daemon_cmd = ['sudo', 'systemctl', 'daemon-reload']
    subprocess.check_call(reload_daemon_cmd)
    enable_service_cmd = ['sudo', 'systemctl', 'enable', 'myservice']
    subprocess.check_call(enable_service_cmd)
    
if __name__ == '__main__':
    logging.info('Start install wireguard...')
    try:
        logging.info('Check if Python user is root...')
        verify_if_is_root()
        logging.info('Installing wireguard...')
        install_wireguard()
        logging.info('Installing flask...')
        install_flask()
        logging.info('Set the app.py to run at reboot...')
        set_app_to_at_restart()
        logging.info('Success')
    except Exception as ex:
        logging.error(ex)
