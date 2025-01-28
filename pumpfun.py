# pumpfun.py
class PumpFunBot:
    def __init__(self, config):
        self.config = config
        self.db = DatabaseManager(config)
        self.analytics = AnalyticsEngine(config)
        self.tg_bot = TradeBot(config, self)
        self.bonkbot = BonkBotClient()
        
    async def analyze_and_trade(self):
        """Main trading pipeline"""
        insights = self.run_pipeline()
        
        # Execute trades based on signals
        for signal in insights.get('buy_signals', []):
            if self.config.TRADE_CONFIRMATION:
                await self.tg_bot.send_alert(
                    f"🚨 BUY Signal: {signal['token']}\n"
                    f"Price: ${signal['price']}\n"
                    f"Score: {signal['score']}/100\n"
                    f"Use /buy {signal['token']} to execute"
                )
            else:
                await self.bonkbot.execute_trade(
                    signal['token'], 
                    'buy',
                    self.config.BONKBOT_API_KEY
                )

    def run(self):
        """Start all services"""
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Start Telegram bot in background
        loop.create_task(self.tg_bot.run())
        
        # Start analysis loop
        while True:
            loop.run_until_complete(self.analyze_and_trade())
            time.sleep(60 * 5)  # Run every 5 minutes