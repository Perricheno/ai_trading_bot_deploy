import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

# Absolute path to the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tickers to train on
tickers = ['GOOGL', 'ORCL', 'NET']

def train_and_save_model(ticker):
    print(f"--- Training model for {ticker} ---")
    
    # 1. Download data
    try:
        data = yf.download(ticker, start="2020-01-01")
        if data.empty:
            print(f"Warning: No data found for {ticker}")
            return 0
    except Exception as e:
        print(f"Error downloading {ticker}: {e}")
        return 0
    
    # 2. Feature Engineering
    df = data[['Close']].copy()
    df['MA_5'] = df['Close'].rolling(window=5).mean()
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['Target'] = df['Close'].shift(-1)
    df = df.dropna()

    if df.empty:
        print(f"Not enough data to train {ticker}")
        return 0

    X = df[['Close', 'MA_5', 'MA_20']]
    y = df['Target']

    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Model Training
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 5. Evaluation
    score = model.score(X_test, y_test)
    accuracy = round(score * 100, 2)

    # 6. Save Model
    model_path = os.path.join(BASE_DIR, f"{ticker}_model.pkl")
    joblib.dump(model, model_path)
    print(f"Model {ticker} saved. Accuracy: {accuracy}%")
    return accuracy

if __name__ == "__main__":
    accuracies = {}
    for t in tickers:
        accuracies[t] = train_and_save_model(t)

    # Save accuracies
    accuracies_path = os.path.join(BASE_DIR, "accuracies.pkl")
    joblib.dump(accuracies, accuracies_path)
    print("\n[SUCCESS] All models trained and saved.")
