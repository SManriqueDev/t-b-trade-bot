from binance_trade_bot.logger import Logger
from binance_trade_bot.config import Config
import tweepy


def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True


class TweetsListener(tweepy.StreamListener):
    def __init__(self, logger: Logger):
        super(TweetsListener, self).__init__()
        self.logger = logger

    def on_connect(self):
        self.logger.info("TweetsListener OnConnected!")

    def on_status(self, status):
        if from_creator(status):
            self.logger.info(status.text)

    def on_error(self, status_code):
        print("Error", status_code)


def main():
    config = Config()
    logger = Logger()
    auth = tweepy.OAuthHandler(config.TWEEPY_CONSUMER_KEY,
                               config.TWEEPY_CONSUMER_SECRET)
    auth.set_access_token(
        config.TWEEPY_ACCESS_TOKEN, config.TWEEPY_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    user = api.get_user("elonmusk")
    stream = TweetsListener(logger)
    streamingApi = tweepy.Stream(auth=api.auth, listener=stream)
    streamingApi.filter(
        follow=[user._json['id_str']],
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
