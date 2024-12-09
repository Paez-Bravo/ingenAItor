import requests
import os

def get_financial_news() -> list:
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    tavily_response = requests.get(
        "https://api.tavily.com/search",
        params={"query": "latest financial market updates"},
        headers={"Authorization": f"Bearer {tavily_api_key}"}
    )
    if tavily_response.status_code != 200:
        raise Exception("Failed to fetch Tavily data")
    return tavily_response.json().get('results', [])
