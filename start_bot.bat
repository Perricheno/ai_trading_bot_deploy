@echo off
echo ====================================================
echo AI TRADING BOT - QUICK START
echo ====================================================
echo.

echo [1/3] Checking/Installing dependencies...
python -m pip install -r requirements.txt

echo.
echo [2/3] Checking for trained models...
if not exist "accuracies.pkl" (
    echo Models not found. Training now...
    python train.py
) else (
    echo Models found. Skipping training.
)

echo.
echo [3/3] Starting the Telegram Bot...
echo Bot is running! Close this window to stop it.
echo.
python main.py

pause
