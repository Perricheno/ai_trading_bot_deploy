# AI Trading Bot (Team Project 2)

This is a Telegram bot that predicts stock prices for GOOGL, ORCL, and NET using a Random Forest Regressor.

## How it works

1.  **Training:** The `train.py` script downloads historical data from Yahoo Finance and trains a machine learning model.
2.  **Inference:** The `main.py` script runs the Telegram bot, listening for user commands to make live predictions.

## Deployment

You can deploy this bot to Render in one click.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**Important:** After clicking the button, Render will ask for your `TELEGRAM_TOKEN`. Paste your bot token there.
