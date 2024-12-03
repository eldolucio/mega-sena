from data_fetcher import DataFetcher
from analyzer import MegaSenaAnalyzer
from generator import CombinationGenerator
from interface import MegaSenaInterface

def main():
    # Initialize components
    fetcher = DataFetcher()
    historical_data = fetcher.fetch_historical_data()
    
    if not historical_data:
        print("Error: Could not fetch historical data")
        return
    
    analyzer = MegaSenaAnalyzer(historical_data)
    generator = CombinationGenerator(analyzer)
    
    # Start the GUI
    app = MegaSenaInterface(generator)
    app.run()

if __name__ == "__main__":
    main()