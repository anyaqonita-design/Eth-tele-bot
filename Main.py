import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")  # Token dari @BotFather

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Saya ETH Price Bot 🚀\n"
        "Ketik /eth untuk melihat harga Ethereum (USD & IDR)."
    )

# /eth
async def eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd,idr"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        usd = data["ethereum"]["usd"]
        idr = data["ethereum"]["idr"]
        await update.message.reply_text(
            f"💰 Harga Ethereum sekarang:\n"
            f"• USD: ${usd:,}\n"
            f"• IDR: Rp{idr:,.0f}"
        )
    except Exception as e:
        await update.message.reply_text("❌ Gagal mengambil harga ETH. Coba lagi nanti.")

if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("Env BOT_TOKEN belum diisi.")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("eth", eth))
    app.run_polling()
