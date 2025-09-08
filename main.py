import requests
from urllib.parse import urlparse, parse_qs
import argparse

class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.nasid = ""
        self.session = requests.Session()

    def get_nasid(self):
        resp = self.session.get("http://www.msftconnecttest.com/redirect", allow_redirects=True)
        login_url = resp.url
        parsed_url = urlparse(login_url)
        query_params = parse_qs(parsed_url.query)
        nasid_list = query_params.get("nasId")
        if nasid_list:
            self.nasid = nasid_list[0]

    def get_csrf(self):
        resp = self.session.get("http://172.30.21.100/api/csrf-token")
        return resp.json().get("csrf_token")

    def login(self):
        self.get_nasid()
        csrf_token = self.get_csrf()
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "x-csrf-token": csrf_token,
        }
        data = (
            f"username={self.username}&password={self.password}"
            f"&switchip=&nasId={self.nasid}&userIpv4=&userMac=&captcha=&captchaId="
        )
        resp = self.session.post(
            "http://172.30.21.100/api/account/login",
            headers=headers,
            data=data
        )
        return resp.text

def main():
    parser = argparse.ArgumentParser(description="WHUT WLAN")
    parser.add_argument("-u", "--user", required=True, help="username")
    parser.add_argument("-p", "--pswd", required=True, help="password")
    args = parser.parse_args()

    client = Login(args.user, args.pswd)
    result = client.login()
    print(result)

if __name__ == "__main__":
    main()
