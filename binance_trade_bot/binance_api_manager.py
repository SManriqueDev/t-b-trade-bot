from binance.client import Client
from .config import Config
from typing import Dict, List


class AllTickers:
    def __init__(self, all_tickers: List[Dict]):
        self.all_tickers = all_tickers

    def get_price(self, ticker_symbol):
        ticker = next(
            (t for t in self.all_tickers if t["symbol"] == ticker_symbol), None)
        return float(ticker["price"]) if ticker else None


class BinanceAPIManager:
    def __init__(self, config: Config):
        self.binance_client = Client(
            config.BINANCE_API_KEY,
            config.BINANCE_API_SECRET_KEY,
            tld=config.BINANCE_TLD,
        )

    def get_account(self):
        return self.binance_client.get_account()

    def get_all_market_tickers(self):
        return AllTickers(self.binance_client.get_all_tickers())
