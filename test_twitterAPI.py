#code to test the twitter API
import tweepy
import configparser
import sys
import webbrowser
import http.server
import functools
import os


config = configparser.ConfigParser()
try:
    config.read_file(open("config.ini", "r"))
    print("Found the config file")
except FileNotFoundError as e:
    print(e)
    print("Please check if the config.ini file is in the root of project")
    sys.exit(1)


# twitter credentials
# kwargs = dict(bearer_token = config.get('TWITTER','bearer_token'),
#                 consumer_key=config.get('TWITTER', 'consumer_key'),
#               consumer_secret=config.get('TWITTER', 'consumer_secret'),
#               access_token=config.get('TWITTER', 'access_token'),
#               access_token_secret=config.get('TWITTER', 'access_token_secret'))

#connection made using python-twitter API
# api = twitter.Api(**kwargs)

#connection made using tweepy API
# client = tweepy.Client(**kwargs)

#List of scopes to request access to
#For more info: https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
scopes = ['offline.access','bookmark.read']

#===========================================================================================================
# twitter_oauth_callback_url_ip = "127.0.0.1"
# twitter_oauth_callback_url_proto = "http"
# # twitter_oath_callback_url_ports_to_try = [8888, 8880, 8080, 9977, 4356, 3307]
# twitter_oath_callback_url_ports_to_try = [8888, 8880, 8080]

# oauth2_user_handler = None
# http_server = None

# class _AuthParametersCaptureRequestHandler(http.server.BaseHTTPRequestHandler):
#     """
#     Minimal handler for build in python3 httpd server. Captures the parameters made from callback URL to be
#     used in continuing OAuth2 authentication flow
#     """

#     auth_response_dict = None

#     # noinspection PyMissingConstructor
#     def __init__(self, *args, auth_response_dict, **kwargs):
#         self.auth_response_dict = auth_response_dict
#         super(http.server.BaseHTTPRequestHandler, self).__init__(*args, **kwargs)

#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-type", "text/html")
#         self.end_headers()
#         self.wfile.write(b"Authorization complete! You can return to app.")
#         self.auth_response_dict["auth_response_path"] = self.path
#         return self


# # This is the one weird part of the process. The built in HTTP Server class does not have a way to pass information
# # about a request it servers back to the main thread. The AuthParametersCaptureRequestHandler class is a hacky way
# # to 'grab' the URL callback parameters when the Twitter OAuth2 flow passes control back to the script
# auth_response_dict = dict()
# AuthCaptureHandler = functools.partial(_AuthParametersCaptureRequestHandler, auth_response_dict=auth_response_dict)


# for twitter_oath_callback_url_port in twitter_oath_callback_url_ports_to_try:

#     # construct a full call back URL out of our parts
#     twitter_oauth_callback_url = f"{twitter_oauth_callback_url_proto}://{twitter_oauth_callback_url_ip}:{twitter_oath_callback_url_port}/"
#     # logging.debug(f"Creating oauth2 helper with callback URL {twitter_oauth_callback_url}")
#     # create a tweepy oauth handler with the current URL
#     oauth2_user_handler = tweepy.OAuth2UserHandler(
#         client_id='OHI2RDl6REJMczFNZXhPQW42VkQ6MTpjaQ',
#         redirect_uri=twitter_oauth_callback_url,
#         scope=scopes,
#         # Client Secret is only necessary if using a confidential client
#         client_secret="rY22-RLbG_vPMiwzdGvUB5azetUCi6w8ghBhH_ePWIU77Ey8WX"
#     )

#     # print(oauth2_user_handler.redirect_uri)
#     # try to create a local http server listening at the callback URL
#     try:
#         http_server = http.server.HTTPServer((twitter_oauth_callback_url_ip, twitter_oath_callback_url_port),
#                                              AuthCaptureHandler)
#         # logging.info(f"HTTP listener bound to {twitter_oauth_callback_url_ip} {twitter_oath_callback_url_port}")
#     except Exception as e:
#         # logging.warning(f"Could not bind HTTP listener to {twitter_oauth_callback_url_ip} {twitter_oath_callback_url_port}. Going to try next port in list")
#         # logging.debug(f"bind exception is '{e}'")
#         continue

#     # HTTP listener was created, so we can break out of the loop trying the list of listening ports
#     break

# # If httpd is None the listener no subitle port was found, have to exit
# if http_server is None:
#     # logging.error("Could not create httpd listener for callback capture. Exiting")
#     print('http server is none')
#     sys.exit(-1)

# # now that the tweepy oauth handler is ready and there is a local http server ready for the callback URL open the
# # auth page at Twitter
# # print(oauth2_user_handler.get_authorization_url())

# webbrowser.open(oauth2_user_handler.get_authorization_url())

# # Wait for the callback request
# http_server.handle_request()
# print("======HERE========")

# access_credentials_dictionary = oauth2_user_handler.fetch_token(auth_response_dict["auth_response_path"])

# client = tweepy.Client(bearer_token=access_credentials_dictionary["access_token"])

# # This call would fail if client object wasn't authenticated
# print(client.get_me(user_auth=False))

#===========================================================================================================

oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id="OHI2RDl6REJMczFNZXhPQW42VkQ6MTpjaQ",
    redirect_uri="http://127.0.0.1:8080",
    scope=scopes,
    # Client Secret is only necessary if using a confidential client
    client_secret="rY22-RLbG_vPMiwzdGvUB5azetUCi6w8ghBhH_ePWIU77Ey8WX"
)

#get the authorization URL
auth_URL = oauth2_user_handler.get_authorization_url()
print(auth_URL)
access_token = oauth2_user_handler.fetch_token(auth_URL)

# try:
#     print(client.get_me())
# except twitter.error.TwitterError as e:
#     print(e)
#     print("Please check the values in the config file")
#     sys.exit(1)

# #expansions to request additional data objects
# #For more info: https://docs.tweepy.org/en/stable/expansions_and_fields.html#expansions-parameter

# expansions = ['author_id']
# print(client.get_bookmarks(expansions=expansions,max_results=10))

