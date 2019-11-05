import urllib.parse
import os
from config import strava_oauth as config
import webbrowser
import socket
from contextlib import closing
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
import os.path
import strava

code = None


class StoppableHttpServer(HTTPServer):

    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=True)
        self.stop = False

    def serve_forever(self):
        while not self.stop:
            self.handle_request()


class StravaOAuth:
    BASE_URL = "https://www.strava.com/oauth/authorize"
    TOKEN_URL = "https://www.strava.com/api/v3/oauth/token"
    RESPONSE_TYPE = "code"
    SCOPE = "activity:read_all"
    APPROVAL_PROMPT = "auto"
    CLIENT_ID = config["client_id"]
    CLIENT_SECRET = config["client_secret"]

    def __init__(self, credentials_path):
        self.tcp_port = self.find_free_tcp_port()
        self.redirect_url = ''.join(["http://localhost:", self.tcp_port])
        self.credentials_path = credentials_path

    def check_credentials(self):
        credentials = None
        if os.path.isfile(self.credentials_path):
            with open(self.credentials_path, "r") as f:
                credentials = json.load(f)
                if strava.StravaAPI.check_token_validity(credentials["access_token"]) is True:
                    return True
        # obtain access_token by using refresh_token
        if credentials is not None:
            refresh_token_ob = self.refresh_token(credentials["refresh_token"])
            if refresh_token_ob is not False:
                credentials["refresh_token"] = refresh_token_ob["refresh_token"]
                credentials["expires_at"] = refresh_token_ob["expires_at"]
                credentials["expires_in"] = refresh_token_ob["expires_in"]
                credentials["access_token"] = refresh_token_ob["access_token"]
                with open(self.credentials_path, "w") as f:
                    json.dump(credentials, f)
                return True
        self.authorize_by_oauth()
        return True

    def prepare_url(self):
        url = ''.join([self.BASE_URL, "?"])

        parameters = {"client_id": self.CLIENT_ID, "redirect_uri": self.redirect_url,
                      "response_type": self.RESPONSE_TYPE, "approval_prompt": self.APPROVAL_PROMPT, "scope": self.SCOPE}
        return ''.join([url, urllib.parse.urlencode(parameters)])

    def authorize_by_oauth(self):
        webbrowser.open(self.prepare_url())
        httpd = StoppableHttpServer(('localhost', int(self.tcp_port)), SimpleHTTPRequestHandler)
        httpd.serve_forever()
        global code
        self.code = code
        self.exchange_code_for_token(self.credentials_path)

    @staticmethod
    def find_free_tcp_port():
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return str(s.getsockname()[1])

    def exchange_code_for_token(self, filename):
        data = dict(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET, code=self.code,
                    grant_type="authorization_code")
        response = requests.post(self.TOKEN_URL, data)
        with open(filename, "w") as f:
            f.write(response.content.decode("ASCII"))

    def refresh_token(self, refresh_token):
        data = dict(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET, refresh_token=refresh_token,
                    grant_type="refresh_token")
        response = requests.post(self.TOKEN_URL, data)
        if response.status_code != 200:
            return False
        return json.loads(response.content.decode("ASCII"))


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Please go back to console program. You can close browser.')
        response = urllib.parse.parse_qs(self.path)
        if 'code' in response:
            global code
            code = response['code']
            self.send_response(200)
            self.server.stop = True


