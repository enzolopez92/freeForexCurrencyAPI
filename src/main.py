from api.forex_client import ForexAPIClient
from utils.html_generator import HTMLGenerator
from typing import Optional, List
import sys

def main(pairs: Optional[List[str]] = None):
    """
    Main function to fetch forex rates and generate a report.
    Args:
        pairs: Optional list of currency pairs to fetch. If None, fetches all supported pairs.
    """
    try:
        client = ForexAPIClient()
        
        # Print supported pairs for reference
        print("Supported currency pairs:", ", ".join(client.get_supported_pairs()))
        
        # Fetch full API response
        result = client.get_rates(pairs)
        
        # Check if the response is valid
        if not result.get("success"):
            print("Failed to fetch data from the API. Check your API key or connection.")
            sys.exit(1)
        
        # Generate and save the HTML report
        html_gen = HTMLGenerator()
        report_html = html_gen.generate_forex_report(result)
        report_path = html_gen.save_report(report_html)
        
        print(f"\nReport generated successfully: {report_path.absolute()}")
        
        # Print transformed rates to the console
        print("\nCurrent Rates:")
        for pair, rate_data in result.get("rates", {}).items():
            print(f"{pair}: {rate_data['rate']:.6f}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # If currency pairs are provided as command-line arguments, use them
    pairs = sys.argv[1:] if len(sys.argv) > 1 else None
    main(pairs)
