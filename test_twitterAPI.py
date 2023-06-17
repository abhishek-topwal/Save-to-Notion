#code to test the twitter API
import twitter
import configparser
import sys
import os


config = configparser.ConfigParser()
try:
    config.read_file(open("config.ini", "r"))
    print("Found the config file")
except FileNotFoundError as e:
    print(e)
    print("Please check if the config.ini file is in the root of project")
    sys.exit(1)


# #twitter credentials
kwargs = dict(consumer_key=config.get('TWITTER', 'consumer_key'),
              consumer_secret=config.get('TWITTER', 'consumer_secret'),
              access_token_key=config.get('TWITTER', 'access_token_key'),
              access_token_secret=config.get('TWITTER', 'access_token_secret'))

# print(type(*kwargs))

api = twitter.Api(**kwargs)

try:
    print(type(api.VerifyCredentials()))
except twitter.error.TwitterError as e:
    print(e)
    print("Please check the values in the config file")
    sys.exit(1)
