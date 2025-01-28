from pumpfun import PumpFunBot
from config import Config

if __name__ == "__main__":
    bot = PumpFunBot(Config())
    bot.run()