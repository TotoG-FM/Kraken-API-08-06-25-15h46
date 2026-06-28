# Kraken Algorithmic Trading Bot — XRP, ETH, SOL, AVAX

A Python-based algorithmic trading bot connected to the Kraken API, combining machine learning models, quantitative risk management, and real-time market data processing.

## Overview

This project implements a full trading pipeline for cryptocurrency markets (XRP, ETH, SOL, AVAX) on 15-minute timeframes. It was built as a personal project to explore quantitative trading strategies and ML-based price prediction.

## Features

- **GRU/LSTM models** for price direction prediction on 15-minute data
- **Monte Carlo simulation** for risk assessment and scenario analysis
- **ARIMA/VAR models** for time series forecasting
- **Sentiment analysis** on news feeds using NLTK
- **Portfolio optimization** with dynamic weight reallocation
- **Risk management** — drawdown limits, stop-loss, position sizing
- **Async API integration** with Kraken via `aiohttp`
- **Flask monitoring dashboard** for real-time performance tracking

## Architecture

The project follows an object-oriented design:

- `PortfolioManager` — manages capital allocation, position tracking, and dynamic rebalancing
- `DataFetcher` — asynchronous data retrieval from Kraken API
- `FeatureEngineer` — technical indicators and feature construction
- `ModelTrainer` — GRU/LSTM training pipeline with backtesting
- `RiskManager` — drawdown monitoring and position limits

## Tech Stack

```
Python 3.10+
pandas, numpy          — data manipulation
TensorFlow/Keras       — GRU/LSTM models
statsmodels            — ARIMA, VAR
aiohttp                — async API calls
NLTK                   — sentiment analysis
scikit-learn           — preprocessing, evaluation
Flask                  — monitoring dashboard
```

## Setup

```bash
# Clone the repo
git clone https://github.com/your-username/kraken-trading-bot.git
cd kraken-trading-bot

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your Kraken API credentials

# Run
python main.py
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```
KRAKEN_API_KEY=your_api_key_here
KRAKEN_SECRET=your_secret_here
```

## Disclaimer

This project is for educational purposes only. It does not constitute financial advice. Cryptocurrency trading involves significant risk of loss.

## Author

Thomas Guran — [LinkedIn](https://linkedin.com/in/your-profile)
