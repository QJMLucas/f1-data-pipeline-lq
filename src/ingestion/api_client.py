import requests
from typing import Any, Dict

from ..retry import exponential_backoff_retry

BASE_URL = "https://api.openf1.org/v1"


class F1APIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a GET request to the API with exponential backoff retry on rate limit."""
        url = f"{self.base_url}/{endpoint}"

        def make_request():
            print(f"API URL: {url}")
            if params:
                print(f"Params: {params}")
            response = self.session.get(url, params=params, timeout=10)
            # response.raise_for_status()
            return response.json()

        try:
            return exponential_backoff_retry(make_request)
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed for {url}: {str(e)}")

    def close(self):
        """Close the session."""
        self.session.close()
