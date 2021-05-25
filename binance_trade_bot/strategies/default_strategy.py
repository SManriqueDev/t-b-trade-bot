import tweepy
from binance_trade_bot.config import Config
from twitter_bot.__main__ import TweetsListener, TwitterAPIManager
from binance_trade_bot.logger import Logger
from binance_trade_bot.binance_api_manager import BinanceAPIManager


class DefaultStrategyListener(TweetsListener):
    def __init__(self, logger: Logger, manager: BinanceAPIManager):
        super(DefaultStrategyListener, self).__init__(logger)
        self.logger = logger
        self.manager = manager
        self.elon_tweeted = False

    def on_status(self, status):
        if self.from_creator(status):
            self.logger.info('Elon Tweet: ' + status.text)
            self.elon_tweeted = True
            all_market_tickets = self.manager.get_all_market_tickers()
            doger_price = all_market_tickets.get_price("DOGEUSDT")
            self.logger("DOGEUSDT: " + str(doger_price))

    def has_elon_tweeted(self):
        return self.elon_tweeted

    def set_elon_tweeted(self, tweeted):
        self.elon_tweeted = tweeted


class Strategy:
    def __init__(self, binance_manager: BinanceAPIManager, logger: Logger, config: Config):
        self.manager = binance_manager
        self.logger = logger
        self.config = config
        self.twitter_manager = TwitterAPIManager(config)
        user_id = self.twitter_manager.get_user_id("Sebasti75432075")
        elon_musk = self.twitter_manager.get_user_id("elonmusk")
        self.stream = DefaultStrategyListener(logger, binance_manager)
        streamingApi = tweepy.Stream(
            auth=self.twitter_manager.get_api_auth(), listener=self.stream)

        streamingApi.filter(
            follow=[user_id, elon_musk],
            is_async=True,
            filter_level="low"
        )

    def scout(self):
        if self.stream.has_elon_tweeted():
            # TODO - Calculate Return of Investment (ROI)
            self.logger.info("Buy!")
            self.stream.set_elon_tweeted(False)
