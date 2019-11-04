import urllib.parse
import os
from config import strava_oauth as oac
import webbrowser
import socket
from contextlib import closing
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json

code = None


class StoppableHttpServer(HTTPServer):

    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=True)
        self.stop = False

    def serve_forever(self):
        while not self.stop:
            self.handle_request()


class StravaOAuth:
    def __init__(self, uri, client_id, response_type="code", approval_prompt="auto",
                 scope="activity:read_all"):
        self.tcp_port = self.find_free_tcp_port()
        self.redirect_url = ''.join(["http://localhost:", self.tcp_port])
        self.base_url = uri
        self.client_id = client_id
        self.response_type = response_type
        self.approval_prompt = approval_prompt
        self.scope = scope

    def prepare_url(self):
        url = ''.join([self.base_url, "?"])

        vars = {"client_id": self.client_id, "redirect_uri": self.redirect_url, "response_type": self.response_type,
                "approval_prompt": self.approval_prompt, "scope": self.scope}
        return ''.join([url, urllib.parse.urlencode(vars)])

    def authorize(self):
        webbrowser.open(self.prepare_url())
        httpd = StoppableHttpServer(('localhost', int(self.tcp_port)), SimpleHTTPRequestHandler)
        httpd.serve_forever()
        global code
        self.code = code

    @staticmethod
    def find_free_tcp_port():
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return str(s.getsockname()[1])

    def exchange_code_for_token(self, filename):
        data = dict(client_id=self.client_id, client_secret=oac["client_secret"], code=self.code,
                    grant_type="authorization_code")
        response = requests.post("https://www.strava.com/oauth/token", data)
        # print(response.content)
        with open(filename, "w") as f:
            json.dump(response.content, f)


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


if __name__ == "__main__":
    OA = StravaOAuth(oac["base_url"], oac["client_id"])
    # OA.prepare_url()
    OA.authorize()
    OA.exchange_code_for_token("strava_credentials.json")
