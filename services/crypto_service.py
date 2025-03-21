"""
Service for interacting with cryptocurrency APIs and data processing.
"""

import requests
import time
import backoff
from datetime import datetime
import logging


from config import COINGECKO_API_URL, CRYPTOCURRENCIES, CURRENCIES, DATA_POINTS, COLLECTION_INTERVAL

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
@backoff.on_exception(backoff.expo, 
                     (requests.exceptions.RequestException, 
                      requests.exceptions.Timeout,
                      requests.exceptions.ConnectionError),
                     max_tries=3)
def make_api_request(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        
        # Check for rate limiting
        if response.status_code == 429:
            # Get retry time from headers, default to 60 seconds if not present
            retry_after = response.headers.get('Retry-After')
            
            if retry_after:
                try:
                    retry_seconds = int(retry_after)
                except ValueError:
                    # If it's not an integer, use a default
                    retry_seconds = 60
            else:
                # If header not present, use a default
                retry_seconds = 60
                
            logger.warning(f"Rate limited. Waiting for {retry_seconds} seconds")
            time.sleep(retry_seconds)
            # Make a recursive call after waiting
            return make_api_request(url, timeout)
            
        # Check response code for other issues
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API returned error: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        # Connection timeout
        logger.error("Request exceeded timeout")
        return None
    except requests.exceptions.ConnectionError:
        # Connection error
        logger.error("Connection error - check network or API endpoint")
        return None
    except requests.exceptions.RequestException as e:
        # Other request errors
        logger.error(f"Request exception: {e}")
        return None
    except ValueError as e:
        # Error parsing JSON
        logger.error(f"JSON parse error: {e}")
        return None
def get_crypto_prices():
    """
    Get current prices for specified cryptocurrencies.
    
    Returns:
        tuple: Current prices for Bitcoin, Ethereum, and Solana in USD
    """
    ids_param = ",".join(CRYPTOCURRENCIES)
    vs_currencies_param = ",".join(CURRENCIES)
    
    url = f"{COINGECKO_API_URL}?ids={ids_param}&vs_currencies={vs_currencies_param}"
    data = make_api_request(url)
    
    if data:
        try:
            # Check if all cryptocurrencies are present
            missing_currencies = [crypto for crypto in CRYPTOCURRENCIES if crypto not in data]
            if missing_currencies:
                logger.warning(f"Missing data for currencies: {missing_currencies}")
                
            # Get prices with checks for data presence
            btc_price = data.get("bitcoin", {}).get("usd", "N/A")
            eth_price = data.get("ethereum", {}).get("usd", "N/A")
            sol_price = data.get("solana", {}).get("usd", "N/A")
            
            # Check data types
            if not isinstance(btc_price, (int, float)) and btc_price != "N/A":
                logger.warning(f"Unexpected price format for BTC: {btc_price}")
            
            return btc_price, eth_price, sol_price
        except Exception as e:
            logger.error(f"Error processing API response: {e}")
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
        
        # Используем функцию make_api_request вместо прямого requests.get
        data = make_api_request(url)
        
        if data:
            try:
                btc_price = data.get("bitcoin", {}).get("usd")
                eth_price = data.get("ethereum", {}).get("usd")
                sol_price = data.get("solana", {}).get("usd")
                
                price_data = {
                    "time": current_time,
                    "bitcoin": btc_price,
                    "ethereum": eth_price,
                    "solana": sol_price,
                }
                
                price_history.append(price_data)
                logger.info(f"Price of BTC: ${btc_price}, ETH: ${eth_price}, SOL: ${sol_price}")
            except Exception as e:
                logger.error(f"Error in data processing: {e}")
        else:
            logger.error("Failed to get API response")
        
        # Sleep between requests except for the last one
        if i < DATA_POINTS - 1:
            logger.info(f"Waiting for {COLLECTION_INTERVAL} seconds")
            time.sleep(COLLECTION_INTERVAL)
    
    return price_history