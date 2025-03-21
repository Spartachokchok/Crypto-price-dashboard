"""
Configuration file for the Crypto Dashboard application.
"""

# API settings
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
CRYPTOCURRENCIES = ["bitcoin", "ethereum", "solana"]
CURRENCIES = ["usd"]

# Data collection settings
DATA_POINTS = 6
COLLECTION_INTERVAL = 60  # seconds between API calls during collection

# Update settings
UPDATE_INTERVAL = 300  # seconds (5 minutes)