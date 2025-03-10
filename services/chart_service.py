"""
Service for creating charts and visualizations.
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
import logging
from matplotlib.dates import DateFormatter

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_price_chart(price_history):
    """
    Create a chart visualizing cryptocurrency price history.
    
    Args:
        price_history (list): List of dictionaries containing price data
    
    Returns:
        bool: True if chart was created successfully, False otherwise
    """
    try:
        # Create DataFrame from price history
        df = pd.DataFrame(price_history)
        df['time'] = pd.to_datetime(df['time'])
        
        # Create chart with 3 subplots (one for each cryptocurrency)
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15), sharex=True)
        
        # Format date on x-axis
        date_format = DateFormatter('%H:%M:%S')
        
        # Bitcoin chart (top subplot)
        ax1.plot(df['time'], df['bitcoin'], 'o-', color='orange', linewidth=2, label='Bitcoin')
        ax1.set_ylabel('Bitcoin Price (USD)', color='orange')
        ax1.tick_params(axis='y', labelcolor='orange')
        ax1.grid(True)
        ax1.legend(loc='upper left')
        ax1.set_title('Bitcoin Price Movement')
        ax1.xaxis.set_major_formatter(date_format)
        
        # Ethereum chart (middle subplot)
        ax2.plot(df['time'], df['ethereum'], 's-', color='blue', linewidth=2, label='Ethereum')
        ax2.set_ylabel('Ethereum Price (USD)', color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')
        ax2.grid(True)
        ax2.legend(loc='upper left')
        ax2.set_title('Ethereum Price Movement')
        ax2.xaxis.set_major_formatter(date_format)
        
        # Solana chart (bottom subplot)
        ax3.plot(df['time'], df['solana'], '^-', color='purple', linewidth=2, label='Solana')
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Solana Price (USD)', color='purple')
        ax3.tick_params(axis='y', labelcolor='purple')
        ax3.grid(True)
        ax3.legend(loc='upper left')
        ax3.set_title('Solana Price Movement')
        ax3.xaxis.set_major_formatter(date_format)
        
        # Improve layout
        plt.tight_layout()
        
        # Make sure static/images folder exists
        os.makedirs('static/images', exist_ok=True)
        
        # Save the chart
        chart_path = os.path.join('static', 'images', 'crypto_prices.png')
        plt.savefig(chart_path)
        plt.close()
        
        logger.info(f"Chart saved to {chart_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error creating chart: {e}")
        return False