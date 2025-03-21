"""
Crypto Dashboard - A Flask application that displays real-time cryptocurrency prices.

This application fetches current prices for Bitcoin, Ethereum, and Solana 
from the CoinGecko API and displays them along with historical price charts.
"""

from flask import Flask, render_template
import time
from datetime import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# Import services
from services.crypto_service import get_crypto_prices, collect_price_history
from services.chart_service import create_price_chart
from config import UPDATE_INTERVAL

# Initialize Flask application
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to store the latest data
crypto_data = {
    "btc_price": "Loading...",
    "eth_price": "Loading...",
    "sol_price": "Loading...",
    "last_update": "Not updated yet",
    "timestamp": int(time.time())
}

def update_data():
    try:
        # Get current prices
        btc, eth, sol = get_crypto_prices()
        
        # Check if we got valid data
        if "N/A" in (btc, eth, sol):
            crypto_data["error_count"] += 1
            logger.warning(f"Incomplete data received. Error count: {crypto_data['error_count']}")
            
            # If too many errors, show warning to user
            if crypto_data["error_count"] > 3:
                crypto_data["status"] = "api_issues"
            
            # Keep the old prices if they exist
            if crypto_data["btc_price"] != "Loading...":
                if btc == "N/A": btc = crypto_data["btc_price"]
                if eth == "N/A": eth = crypto_data["eth_price"]
                if sol == "N/A": sol = crypto_data["sol_price"]
        else:
            # Reset error counter if successful
            crypto_data["error_count"] = 0
            crypto_data["status"] = "ok"
            crypto_data["last_successful_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update data
        crypto_data["btc_price"] = btc
        crypto_data["eth_price"] = eth
        crypto_data["sol_price"] = sol
        crypto_data["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.error(f"Error during data update: {e}")
        crypto_data["error_count"] += 1
        crypto_data["status"] = "error"
    """Background task to update cryptocurrency data and charts"""
    logger.info("Starting data update")
    
    # Get current prices
    btc, eth, sol = get_crypto_prices()
    
    # Update global data
    crypto_data["btc_price"] = btc
    crypto_data["eth_price"] = eth
    crypto_data["sol_price"] = sol
    crypto_data["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    crypto_data["timestamp"] = int(time.time())
    
    # Collect price history and create chart
    price_history = collect_price_history()
    if price_history and len(price_history) > 0:
        create_price_chart(price_history)
    
    logger.info(f"Data update completed at {crypto_data['last_update']}")

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_data, trigger="interval", seconds=UPDATE_INTERVAL)
scheduler.start()

# Ensure scheduler shuts down when app exits
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    """Render the main dashboard page"""
    # If this is first run, update data immediately
    if crypto_data["btc_price"] == "Loading...":
        update_data()
    
    # Render the template with the latest data
    return render_template(
        'index.html',
        btc_price=crypto_data["btc_price"],
        eth_price=crypto_data["eth_price"],
        sol_price=crypto_data["sol_price"],
        last_update=crypto_data["last_update"],
        timestamp=crypto_data["timestamp"]
    )

if __name__ == '__main__':
    app.run(debug=True)