
# Crypto Price Dashboard

A real-time cryptocurrency dashboard that tracks prices for Bitcoin, Ethereum, and Solana using the CoinGecko API.


## Features

- Live price updates for BTC, ETH, and SOL
- Automatic data refresh every 5 minutes
- Historical price charts
- Responsive design

## Technology Stack

- **Backend**: Python, Flask
- **Data Visualization**: Matplotlib, Pandas
- **Scheduling**: APScheduler
- **API Integration**: CoinGecko API
- **Frontend**: HTML, CSS

## Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/crypto-price-dashboard.git
   cd crypto-price-dashboard
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run the application
   ```
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── static/                # Static files
│   ├── css/               # CSS stylesheets
│   │   └── style.css
│   ├── js/                # JavaScript files
│   │   └── app.js
│   └── images/            # Generated charts
├── templates/             # HTML templates
│   ├── base.html
│   └── index.html
└── services/              # Application services
    ├── crypto_service.py  # Cryptocurrency API service
    └── chart_service.py   # Chart generation service
```

## Configuration

You can modify the application settings in `config.py`:

- `UPDATE_INTERVAL`: Time between data updates (in seconds)
- `DATA_POINTS`: Number of data points to collect for charts
- `COLLECTION_INTERVAL`: Time between API calls during data collection

## License

[MIT License](LICENSE)

## Acknowledgements

- [CoinGecko API](https://www.coingecko.com/en/api) for cryptocurrency data
- [Flask](https://flask.palletsprojects.com/) web framework
- [Matplotlib](https://matplotlib.org/) for data visualization
