# src/api/forex_client.py
import requests
import os
from typing import List, Dict, Optional, Union
from dotenv import load_dotenv
from datetime import datetime

class ForexAPIClient:
    """Client for the Currency Layer API"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment variables
        self.api_key = os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables")
            
        self.base_url = os.getenv('BASE_URL', 'http://apilayer.net/api/live')
        
        # Update supported pairs to match your actual currency pairs
        self.supported_pairs = [
            "EURUSD", "GBPUSD", "USDJPY", 
            "AUDUSD", "USDCHF", "NZDUSD", 
            "USDCAD", "USDZAR"
        ]

    def get_rates(self, pairs: Optional[Union[str, List[str]]] = None) -> Dict:
        if pairs is None:
            pairs = self.supported_pairs
        elif isinstance(pairs, str):
            pairs = [pairs]

        # Validate requested pairs
        invalid_pairs = [p for p in pairs if p not in self.supported_pairs]
        if invalid_pairs:
            raise ValueError(f"Unsupported currency pairs: {invalid_pairs}")

        # Prepare API parameters
        params = {
            "access_key": self.api_key,
            "source": "USD",
            "format": 1
        }

        response = requests.get(self.base_url, params=params)
        
        # Debugging response
        print(f"Raw API response: {response.text}")
        
        try:
            data = response.json()
            print(f"Parsed JSON: {data}")  # Debugging parsed data
        except ValueError:
            raise ValueError("Invalid JSON response from API")

        if not data.get("success", False):
            raise Exception(f"API returned error: {data.get('error', {}).get('info', 'Unknown error')}")

        timestamp = data.get("timestamp", int(datetime.now().timestamp()))
        quotes = data.get("quotes", {})
        
        # Transform the response to match the expected format
        rates = {}
        for pair in pairs:
            if pair.startswith("USD"):
                # Direct USD quote (e.g., USDJPY)
                currency = pair[3:]
                quote_key = f"USD{currency}"
                if quote_key in quotes:
                    rates[pair] = {
                        "rate": quotes[quote_key],
                        "timestamp": timestamp
                    }
            else:
                # Inverse quote (e.g., EURUSD)
                currency = pair[:3]
                quote_key = f"USD{currency}"
                if quote_key in quotes:
                    rates[pair] = {
                        "rate": 1 / quotes[quote_key],  # Invert the rate
                        "timestamp": timestamp
                    }

        if not rates:
            print("Warning: No rates found in API response")
            
        result = {
        "success": data.get("success", False),
        "terms": data.get("terms", "N/A"),
        "privacy": data.get("privacy", "N/A"),
        "timestamp": timestamp,
        "source": data.get("source", "USD"),
        "rates": rates,  # Transformed and filtered rates
        "all_quotes": quotes  # Original quotes for completeness
    }
        return result

    def get_supported_pairs(self) -> List[str]:
        """Return list of supported currency pairs"""
        return self.supported_pairs.copy()
