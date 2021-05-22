import configparser
import os

CFG_FL_NAME = "app.cfg"
USER_CFG_SECTION = "BINANCE_USER_CONFIG"
TWEEPY_CFG_SECTION = "TWEEPY_CONFIG"


class Config:
    def __init__(self):
        config = configparser.ConfigParser()
        config["DEFAULT"] = {
            "scout_sleep_time": "5",
            "tld": "com",
            "strategy": "default"
        }

        if not os.path.exists(CFG_FL_NAME):
            print(
                "app.cfg not found!. Assuming default config...")
            config[USER_CFG_SECTION] = {}
            config[TWEEPY_CFG_SECTION] = {}
        else:
            config.read(CFG_FL_NAME)

        self.BINANCE_API_KEY = config.get(
            USER_CFG_SECTION, "api_key")
        self.BINANCE_API_SECRET_KEY = config.get(
            USER_CFG_SECTION, "api_secret_key")
        self.BINANCE_TLD = config.get(USER_CFG_SECTION, "tld")
        self.STRATEGY = config.get(
            USER_CFG_SECTION, "strategy")

        self.SCOUT_SLEEP_TIME = int(config.get(
            USER_CFG_SECTION, "scout_sleep_time"))

        self.TWEEPY_CONSUMER_KEY = config.get(
            TWEEPY_CFG_SECTION, "consumer_key")
        self.TWEEPY_CONSUMER_SECRET = config.get(
            TWEEPY_CFG_SECTION, "consumer_secret")
        self.TWEEPY_ACCESS_TOKEN = config.get(
            TWEEPY_CFG_SECTION, "access_token")
        self.TWEEPY_ACCESS_TOKEN_SECRET = config.get(
            TWEEPY_CFG_SECTION, "access_token_secret")
