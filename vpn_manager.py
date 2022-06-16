
from datetime import datetime, timedelta
import email
import time
import yagmail
from database.repository.client_dao import ClientDao

from database.repository.vpn_dao import VpnDao
from service.service import Service

def run():
    #de completat sau (cel mai bine) de luat informatiile contului din DB
    email = ''
    password = ''
    yag = yagmail.SMTP(email, password)
    while True:
        vpns_email = VpnDao.get_all_vpns_which_needs_reminder_email()
        contents = [
          "Your VPN will expire in 10 days. Check your subscription at your account main page."
        ]
        for vpn in vpns_email:
            print(vpn)
            client = ClientDao.get_by_id(vpn.client_id)
            try:
                yag.send(client.mail, 'subject', contents)
                print(vpn.id)
                VpnDao.set_subscribe(vpn.id, False)
                print("Email sent successfully")
            except Exception as ex:
                print(f"Error, email was not sent {ex}")

        vpns = VpnDao.get_all_expired_vpns()
        for vpn in vpns:
            try:
                Service.revoke_client(vpn.client_id, vpn.server_id, vpn.id)
            except Exception as e:
                print(str(e))
        # time.sleep(86400)
        time.sleep(10)


if __name__ == '__main__':
    run()