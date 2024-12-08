import requests

def get_financial_updates() -> str:
    tavily_api_key = "tvly-YOUR_API_KEY"
    tavily_response = requests.get(
        "https://api.tavily.com/search",
        params={"query": "latest financial market updates"},
        headers={"Authorization": f"Bearer {tavily_api_key}"}
    )
    return tavily_response.json().get('results', [])[0].get('snippet', '') if tavily_response.json().get('results') else 'No updates available'
