import logging
import yfinance as yf
import joblib
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Absolute path to the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration
# Tries to get the token from Environment Variables (Best Practice for Cloud)
# If not found, it falls back to your hardcoded token (For local testing)
TOKEN = os.getenv("TELEGRAM_TOKEN", "8407735906:AAFhnz7OzMjF-dnGVe-E8xgOckQj-r451KA")

TICKERS = ['GOOGL', 'ORCL', 'NET']

# Load Accuracies
try:
    accuracies_path = os.path.join(BASE_DIR, "accuracies.pkl")
    accuracies = joblib.load(accuracies_path)
except:
    accuracies = {"GOOGL": 0, "ORCL": 0, "NET": 0}

# Logging Configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I am the AI Trading Bot (Team Project 2).\n\n"
        "I predict stock prices for Alphabet, Oracle, and Cloudflare.\n\n"
        "📌 Commands:\n"
        "/predict [ticker] - Forecast for tomorrow\n"
        "/status [ticker] - Current price and model confidence"
    )

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please enter a ticker. Example: /predict GOOGL")
        return

    ticker = context.args[0].upper()
    if ticker not in TICKERS:
        await update.message.reply_text(f"⚠️ I only know: {', '.join(TICKERS)}")
        return

    try:
        # Fetch live data
        data = yf.download(ticker, period="30d")
        
        # Explicit type casting to float to avoid numpy errors
        last_close = float(data['Close'].iloc[-1])
        ma5 = float(data['Close'].rolling(window=5).mean().iloc[-1])
        ma20 = float(data['Close'].rolling(window=20).mean().iloc[-1])

        features = [[last_close, ma5, ma20]]

        # Load Model
        model_path = os.path.join(BASE_DIR, f"{ticker}_model.pkl")
        model = joblib.load(model_path)
        
        # Predict
        prediction = model.predict(features)[0]
        trend = "🚀 UP" if prediction > last_close else "📉 DOWN"
        
        message = (
            f"🤖 *Forecast for {ticker}*\n\n"
            f"💰 Current Price: `${last_close:.2f}`\n"
            f"🔮 Predicted Tomorrow: `${prediction:.2f}`\n"
            f"📊 Direction: {trend}\n"
            f"🎯 Confidence (R²): `{accuracies.get(ticker, 0)}%`"
        )
        await update.message.reply_markdown(message)
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        await update.message.reply_text("❌ An error occurred during prediction. The model might not be trained or data fetch failed.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please enter a ticker. Example: /status ORCL")
        return

    ticker = context.args[0].upper()
    if ticker not in TICKERS:
        await update.message.reply_text("Ticker not supported.")
        return

    try:
        data = yf.Ticker(ticker).history(period="1d")
        current_price = data['Close'].iloc[-1]

        message = (
            f"📊 *Status for {ticker}*\n"
            f"Current Market Price: `${current_price:.2f}`\n"
            f"Model Confidence: `{accuracies.get(ticker, 0)}%`"
        )
        await update.message.reply_markdown(message)
    except Exception as e:
        await update.message.reply_text("Could not fetch status.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    app.add_handler(CommandHandler("status", status))
    
    print("--- Bot is running ---")
    app.run_polling()
