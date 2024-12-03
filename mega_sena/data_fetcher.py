import urllib.request
import json
from datetime import datetime

class DataFetcher:
    def __init__(self):
        self.base_url = "https://loteriascaixa-api.herokuapp.com/api/mega-sena"
    
    def fetch_historical_data(self):
        """Fetch historical Mega-Sena data from the API"""
        try:
            with urllib.request.urlopen(self.base_url) as response:
                data = json.loads(response.read())
                return self._process_data(data)
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []
    
    def _process_data(self, raw_data):
        """Process the raw API data into a structured format"""
        processed_data = []
        for draw in raw_data:
            numbers = [int(num) for num in draw.get('dezenas', [])]
            if numbers:
                processed_data.append({
                    'concurso': draw.get('concurso'),
                    'data': draw.get('data'),
                    'numbers': sorted(numbers)
                })
        return processed_data