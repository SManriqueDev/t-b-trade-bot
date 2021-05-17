from binance_trade_bot.logger import Logger
from binance_trade_bot.binance_api_manager import BinanceAPIManager


class Strategy:
    def __init__(self, binance_manager: BinanceAPIManager, logger: Logger):
        self.manager = binance_manager
        self.logger = logger

    def scout(self):
        list_of_tickets = self.manager.get_all_market_tickers()
        doge_price = list_of_tickets.get_price("DOGEUSDT")
        self.logger.info("DOGEUSDT")
        self.logger.info(str(doge_price))
