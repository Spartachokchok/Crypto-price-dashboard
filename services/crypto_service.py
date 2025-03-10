"""
Service for interacting with cryptocurrency APIs and data processing.
"""

import requests
import time
from datetime import datetime
import logging
from config import COINGECKO_API_URL, CRYPTOCURRENCIES, CURRENCIES, DATA_POINTS, COLLECTION_INTERVAL

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_crypto_prices():
    """
    Get current prices for specified cryptocurrencies.
    
    Returns:
        tuple: Current prices for Bitcoin, Ethereum, and Solana in USD
    """
    try:
        ids_param = ",".join(CRYPTOCURRENCIES)
        vs_currencies_param = ",".join(CURRENCIES)
        
        url = f"{COINGECKO_API_URL}?ids={ids_param}&vs_currencies={vs_currencies_param}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            btc_price = data["bitcoin"]["usd"]
            eth_price = data["ethereum"]["usd"]
            sol_price = data["solana"]["usd"]
            
            logger.info(f"Fetched prices: BTC=${btc_price}, ETH=${eth_price}, SOL=${sol_price}")
            return btc_price, eth_price, sol_price
        else:
            logger.error(f"API Error: Status code {response.status_code}")
            return "N/A", "N/A", "N/A"
            
    except Exception as e:
        logger.error(f"Error fetching prices: {e}")
        return "N/A", "N/A", "N/A"

def collect_price_history():
    """
    Collect price history for specified cryptocurrencies.
    
    Returns:
        list: List of dictionaries containing price data over time
    """
    ids_param = ",".join(CRYPTOCURRENCIES)
    vs_currencies_param = ",".join(CURRENCIES)
    url = f"{COINGECKO_API_URL}?ids={ids_param}&vs_currencies={vs_currencies_param}"
    
    price_history = []

    for i in range(DATA_POINTS):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Processing request {i+1} of {DATA_POINTS} at {current_time}")
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                btc_price = data["bitcoin"]["usd"]
                eth_price = data["ethereum"]["usd"]
                sol_price = data["solana"]["usd"]
                
                price_data = {
                    "time": current_time,
                    "bitcoin": btc_price,
                    "ethereum": eth_price,
                    "solana": sol_price,
                }
                
                price_history.append(price_data)
                logger.info(f"Price of BTC: ${btc_price}, ETH: ${eth_price}, SOL: ${sol_price}")
            else:
                logger.error(f"API Error: Status code {response.status_code}")
        
        except Exception as e:
            logger.error(f"Error in data collection: {e}")
        
        # Sleep between requests except for the last one
        if i < DATA_POINTS - 1:
            logger.info(f"Waiting for {COLLECTION_INTERVAL} seconds")
            time.sleep(COLLECTION_INTERVAL)
        else:
            logger.info("Data collection completed")
    
    return price_history