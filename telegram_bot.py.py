# telegram_bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

class TradeBot:
    def __init__(self, config, pumpfun_bot):
        self.config = config
        self.pumpfun = pumpfun_bot
        self.app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
        
        # Register handlers
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("buy", self.buy))
        self.app.add_handler(CommandHandler("sell", self.sell))
        self.app.add_handler(CallbackQueryHandler(self.button_handler))
        self.app.add_handler(MessageHandler(filters.TEXT, self.message_handler))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🚀 PumpFun Trading Bot Ready\n\n"
            "Commands:\n"
            "/buy [token] - Execute buy order\n"
            "/sell [token] - Execute sell order\n"
            "/portfolio - Show current holdings\n"
            "/alerts - Latest market alerts"
        )

    async def buy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        token = context.args[0] if context.args else None
        if not token:
            await update.message.reply_text("Please specify a token address")
            return

        keyboard = [
            [InlineKeyboardButton("Confirm Buy", callback_data=f"buy_confirm_{token}")],
            [InlineKeyboardButton("Cancel", callback_data="cancel")]
        ]
        
        await update.message.reply_text(
            f"Confirm buy order for {token}?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        data = query.data
        
        if data.startswith("buy_confirm_"):
            token = data.split("_")[2]
            # Execute trade through BonkBot
            success = await BonkBotClient.execute_trade(
                token=token,
                action="buy",
                api_key=self.config.BONKBOT_API_KEY
            )
            if success:
                await query.edit_message_text(f"✅ Buy order executed for {token}")
                # Store trade in database
                self.pumpfun.db.log_trade(token, "buy")
            else:
                await query.edit_message_text("❌ Trade execution failed")

        elif data == "cancel":
            await query.edit_message_text("Trade canceled")

    async def send_alert(self, message):
        await self.app.bot.send_message(
            chat_id=self.config.TELEGRAM_CHAT_ID,
            text=message
        )

    def run(self):
        self.app.run_polling()