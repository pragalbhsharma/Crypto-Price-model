import requests
import pandas as pd

# Step 1: Fetch Cryptocurrency Data
def fetch_crypto_data():
    """
    Fetches real-time cryptocurrency data from CoinGecko's public API.
    The API returns details about the top cryptocurrencies based on market capitalization.
    """
    # API endpoint to get cryptocurrency market data
    url = "https://api.coingecko.com/api/v3/coins/markets"
    
    # Parameters to specify currency (INR) and sorting criteria (by market cap)
    params = {
        "vs_currency": "inr",        # Currency for prices (Indian Rupee)
        "order": "market_cap_desc", # Order by descending market cap
        "per_page": 10,             # Fetch only the top 10 cryptocurrencies
        "page": 1                   # Fetch data from the first page
    }
    
    # Make a GET request to the API
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the JSON response if successful
    else:
        # Raise an error if the API call fails
        raise Exception(f"Failed to fetch data: {response.status_code}")

# Step 2: Process the Data
def process_data(data):
    """
    Processes the JSON data into a pandas DataFrame and extracts relevant columns.
    """
    # Convert JSON data into a pandas DataFrame for easier analysis
    df = pd.DataFrame(data)
    
    # Select only the columns we need
    df = df[["name",                # Name of the cryptocurrency (e.g., Bitcoin)
             "current_price",       # Current price in INR
             "high_24h",            # Highest price in the last 24 hours
             "low_24h",             # Lowest price in the last 24 hours
             "price_change_percentage_24h"]]  # Percentage price change in 24 hours
    
    # Return the processed DataFrame
    return df

# Step 3: Main Function to Combine Steps
def main():
    """
    Main function to fetch, process, and display cryptocurrency data.
    """
    try:
        # Fetch data from the API
        crypto_data = fetch_crypto_data()
        
        # Process the fetched data into a DataFrame
        df = process_data(crypto_data)
        
        # Display the top 10 cryptocurrencies in a tabular format
        print("Top 10 Cryptocurrencies (by Market Cap):\n")
        print(df)
        
        # Display the top 5 gainers (sorted by percentage price change in 24 hours)
        print("\nTop 5 Gainers:")
        print(df.nlargest(5, "price_change_percentage_24h"))  # Find the top 5 cryptocurrencies with the highest gains
    except Exception as e:
        # Print the error message if something goes wrong
        print(e)

# Entry point for the script
if __name__ == "__main__":
    main()
