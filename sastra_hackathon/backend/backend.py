import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# 🔑 API Configurations
API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"
GOLD_API_URL = "https://api.metals.live/v1/spot"  # Free gold price API
NEWS_API_KEY = "5254080d13eb4b4d8c7e425785d03eff"  # Replace with a valid NewsAPI key
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handles market trend analysis queries from frontend."""
    try:
        data = request.json
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Query is required"}), 400

        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": query}],
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, json=payload, headers=headers)
        print("Groq API Response:", response.status_code, response.text)

        if response.status_code == 200:
            result = response.json()
            message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            return jsonify({"choices": [{"message": {"content": message}}]}) if message else jsonify({"error": "No insights found"}), 404
        else:
            return jsonify({"error": "API request failed", "details": response.text}), response.status_code

    except Exception as e:
        print("Server Error:", str(e))
        return jsonify({"error": "Internal server error"}), 500

@app.route('/live_trends', methods=['GET'])
def get_live_trends():
    """Fetches real-time market trends using Yahoo Finance."""
    try:
        stock_symbols = ["AAPL", "TSLA", "GOOGL", "AMZN"]
        stock_data = {}
        for symbol in stock_symbols:
            stock = yf.Ticker(symbol)
            stock_info = stock.history(period="1d")
            latest_price = stock_info['Close'].iloc[-1] if not stock_info.empty else "N/A"
            stock_data[symbol] = latest_price
        return jsonify({"market_trends": stock_data})
    except Exception as e:
        print("Live Trends Error:", str(e))
        return jsonify({"error": "Failed to fetch market trends"}), 500

@app.route('/gold_price', methods=['GET'])
def get_gold_price():
    """Fetches real-time gold prices."""
    try:
        response = requests.get(GOLD_API_URL)
        if response.status_code == 200:
            gold_data = response.json()
            gold_price = gold_data[0].get("gold", "N/A")
            return jsonify({"gold_price": gold_price})
        else:
            return jsonify({"error": "Failed to fetch gold prices"}), response.status_code
    except Exception as e:
        print("Gold Price Error:", str(e))
        return jsonify({"error": "Failed to fetch gold prices"}), 500

@app.route('/news', methods=['GET'])
def get_financial_news():
    """Fetches the latest financial news headlines."""
    try:
        params = {
            "category": "business",
            "country": "us",
            "apiKey": NEWS_API_KEY
        }
        response = requests.get(NEWS_API_URL, params=params)
        if response.status_code == 200:
            news_data = response.json()
            headlines = [article["title"] for article in news_data.get("articles", [])][:5]
            return jsonify({"financial_news": headlines})
        else:
            return jsonify({"error": "Failed to fetch news"}), response.status_code
    except Exception as e:
        print("News Fetch Error:", str(e))
        return jsonify({"error": "Failed to fetch news"}), 500

if __name__ == '__main__':
    app.run(debug=True)
