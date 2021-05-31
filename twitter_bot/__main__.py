from binance_trade_bot.logger import Logger
from binance_trade_bot.config import Config
from queue import Queue
from threading import Thread
import tweepy


class TweetsListener(tweepy.StreamListener):
    def __init__(self, logger: Logger, q=Queue()):
        super(TweetsListener, self).__init__()
        self.logger = logger
        self.q = q
        for i in range(8):
            t = Thread(target=self.do_stuff)
            t.daemon = True
            t.start()

    def on_status(self, status):
        self.q.put(status, timeout=5)

    def on_connect(self):
        self.logger.info("Websocket connected!")

    def on_error(self, status_code):
        print("On error!")
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False
        # returning non-False reconnects the stream, with backoff.

    def do_stuff(self):
        while True:
            status = self.q.get()
            self.do_something(status)
            self.q.task_done()

    def from_creator(self, status):
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


class TwitterListener(TweetsListener):
    def __init__(self, logger: Logger):
        super(TwitterListener, self).__init__(logger)
        self.logger = logger


class TwitterAPIManager():
    def __init__(self, config: Config):
        auth = tweepy.OAuthHandler(config.TWEEPY_CONSUMER_KEY,
                                   config.TWEEPY_CONSUMER_SECRET)
        auth.set_access_token(
            config.TWEEPY_ACCESS_TOKEN, config.TWEEPY_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)

    def get_user(self, userName):
        return self.api.get_user(userName)

    def get_api_auth(self):
        return self.api.auth

    def get_user_id(self, userName):
        return self.api.get_user(userName)._json['id_str']


def main():
    config = Config()
    logger = Logger()
    twitter_manager = TwitterAPIManager(config)
    user_id = twitter_manager.get_user_id("elonmusk")
    stream = TwitterListener(logger)
    streamingApi = tweepy.Stream(
        auth=twitter_manager.get_api_auth(), listener=stream)
    streamingApi.filter(
        follow=[user_id],
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
