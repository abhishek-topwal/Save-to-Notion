import base64
import hashlib
import configparser
import sys
import os
import webbrowser
import functools
import http.server
import json
import requests
import re
from requests.auth import AuthBase, HTTPBasicAuth
from requests_oauthlib import OAuth2Session

config = configparser.ConfigParser()
try:
    config.read_file(open("config.ini", "r"))
    print("Found the config file")
except FileNotFoundError as e:
    print(e)
    print("Please check if the config.ini file is in the root of project")
    sys.exit(1)

# First, you will need to enable OAuth 2.0 in your App’s auth settings in the Developer Portal to get your client ID.
# Inside your terminal you will need to set an enviornment variable
# export CLIENT_ID='your-client-id'
# client_id = os.environ.get("CLIENT_ID")
client_id  = config.get('TWITTER', 'client_id')

# If you have selected a type of App that is a confidential client you will need to set a client secret.
# Confidential Clients securely authenticate with the authorization server.

# Remove the comment on the following line if you are using a confidential client
# client_secret = os.environ.get("CLIENT_SECRET")
client_secret = config.get('TWITTER', 'client_secret')

# Replace the following URL with your callback URL, which can be obtained from your App's auth settings.
redirect_uri = "http://127.0.0.1:8888/oauth/twitter"

# Set the scopes
scopes = ["bookmark.read", "tweet.read", "users.read", "offline.access"]

# Create a code verifier
code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

# Create a code challenge
code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

# Start an OAuth 2.0 session
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)

oauth2_user_handler = None
http_server = None

class _AuthParametersCaptureRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    Minimal handler for build in python3 httpd server. Captures the parameters made from callback URL to be
    used in continuing OAuth2 authentication flow
    """

    auth_response_dict = None

    # noinspection PyMissingConstructor
    def __init__(self, *args, auth_response_dict, **kwargs):
        self.auth_response_dict = auth_response_dict
        super(http.server.BaseHTTPRequestHandler, self).__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Authorization complete! You can return to app.")
        self.auth_response_dict["auth_response_path"] = self.path
        return self


# This is the one weird part of the process. The built in HTTP Server class does not have a way to pass information
# about a request it servers back to the main thread. The AuthParametersCaptureRequestHandler class is a hacky way
# to 'grab' the URL callback parameters when the Twitter OAuth2 flow passes control back to the script
auth_response_dict = dict()
AuthCaptureHandler = functools.partial(_AuthParametersCaptureRequestHandler, auth_response_dict=auth_response_dict)

# try to create a local http server listening at the callback URL
http_server = http.server.HTTPServer(('127.0.0.1',8888),
                                             AuthCaptureHandler)


auth_url = "https://twitter.com/i/oauth2/authorize"
authorization_url, state = oauth.authorization_url(
    auth_url, code_challenge=code_challenge, code_challenge_method="S256"
)

# now that the tweepy oauth handler is ready and there is a local http server ready for the callback URL open the
# auth page at Twitter
webbrowser.open((authorization_url))

# Wait for the callback request
http_server.handle_request()

# Fetch your access token
token_url = "https://api.twitter.com/2/oauth2/token"

# The following line of code will only work if you are using a type of App that is a public client
auth = False

# Please remove the comment on the following line if you are using a type of App that is a confidential client
auth = HTTPBasicAuth(client_id, client_secret)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
token = oauth.fetch_token(
    token_url=token_url,
    authorization_response=auth_response_dict['auth_response_path'],
    auth=auth,
    client_id=client_id,
    include_client_id=True,
    code_verifier=code_verifier,
)

# Your access token
access = token["access_token"]

# Make a request to the users/me endpoint to get your user ID
user_me = requests.request(
    "GET",
    "https://api.twitter.com/2/users/me",
    headers={"Authorization": "Bearer {}".format(access)},
).json()
user_id = user_me["data"]["id"]
print(user_id)


# Make a request to the bookmarks url
# url = "https://api.twitter.com/2/users/{}/bookmarks".format(user_id)
# headers = {
#     "Authorization": "Bearer {}".format(access),
#     "User-Agent": "BookmarksSampleCode",
# }
# response = requests.request("GET", url, headers=headers)
# if response.status_code != 200:
#     raise Exception(
#         "Request returned an error: {} {}".format(response.status_code, response.text)
#     )
# print("Response code: {}".format(response.status_code))
# json_response = response.json()
# print(json.dumps(json_response, indent=4, sort_keys=True))