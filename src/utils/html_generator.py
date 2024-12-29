# src/utils/html_generator.py
from datetime import datetime
from pathlib import Path
from typing import Dict

class HTMLGenerator:
    @staticmethod
    def generate_forex_report(result: Dict) -> str:
        """Generate a comprehensive HTML report for the forex API response."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract metadata
        success = result.get("success", "N/A")
        terms = result.get("terms", "N/A")
        privacy = result.get("privacy", "N/A")
        timestamp = result.get("timestamp", "N/A")
        source = result.get("source", "USD")
        rates = result.get("rates", {})
        all_quotes = result.get("all_quotes", {})

        # Format the timestamp
        formatted_timestamp = (
            datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            if timestamp != "N/A" else "N/A"
        )

        # Start HTML content
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Forex API Detailed Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }}
        th {{
            background-color: #f4f4f4;
        }}
        h1, h2 {{
            margin-bottom: 10px;
        }}
        p {{
            margin: 5px 0;
        }}
        .json-data {{
            white-space: pre-wrap;
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Forex API Report</h1>
        <p><strong>Generated:</strong> {current_time}</p>
        <p><strong>Success:</strong> {success}</p>
        <p><strong>Terms:</strong> <a href="{terms}" target="_blank">Terms of Service</a></p>
        <p><strong>Privacy:</strong> <a href="{privacy}" target="_blank">Privacy Policy</a></p>
        <p><strong>Source Currency:</strong> {source}</p>
        <p><strong>Timestamp:</strong> {formatted_timestamp}</p>
        
        <h2>Filtered Rates</h2>"""
        
        if rates:
            html += """
            <table>
                <tr>
                    <th>Currency Pair</th>
                    <th>Exchange Rate</th>
                </tr>"""
            for pair, rate_data in sorted(rates.items()):
                html += f"""
                <tr>
                    <td>{pair}</td>
                    <td>{rate_data['rate']:.6f}</td>
                </tr>"""
            html += """
            </table>"""
        else:
            html += "<p>No filtered rates available.</p>"

        html += """
        <h2>All Quotes</h2>"""
        
        if all_quotes:
            html += """
            <table>
                <tr>
                    <th>Currency Pair</th>
                    <th>Exchange Rate</th>
                </tr>"""
            for pair, rate in sorted(all_quotes.items()):
                html += f"""
                <tr>
                    <td>{pair}</td>
                    <td>{rate:.6f}</td>
                </tr>"""
            html += """
            </table>"""
        else:
            html += "<p>No quotes available.</p>"

        html += """
    </div>
</body>
</html>"""

        return html


    @staticmethod
    def save_report(html_content: str, filename: str = None) -> Path:
        """Save the HTML report to the reports directory"""
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        if filename is None:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"forex_report_{timestamp}.html"
            
        report_path = reports_dir / filename
        report_path.write_text(html_content)
        return report_path
