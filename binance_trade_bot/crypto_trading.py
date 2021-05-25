from binance_trade_bot.logger import Logger
from binance_trade_bot.strategies import get_strategy
from binance_trade_bot.scheduler import SafeScheduler
import time
from binance_trade_bot.config import Config
from binance_trade_bot.binance_api_manager import BinanceAPIManager


def main():
    logger = Logger()
    logger.info("Starting...")
    config = Config()
    manager = BinanceAPIManager(config)
    try:
        _ = manager.get_account()
    except Exception as e:
        print(
            "Couldn't access Binance API - API keys may be wrong or lack sufficient permissions")
        return
    strategy = get_strategy(config.STRATEGY)

    trader = strategy(manager, logger, config)
    schedule = SafeScheduler(logger)
    schedule.every(config.SCOUT_SLEEP_TIME).seconds.do(
        trader.scout).tag("searching for good trading opportunities")

    while True:
        schedule.run_pending()
        time.sleep(1)
