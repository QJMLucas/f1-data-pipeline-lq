from .api_client import F1APIClient
from ..storage.parquet_writer import write_to_parquet


def get_drivers(driver_number=None, session_key=None):
    """Fetch drivers data from OpenF1 API and write to parquet."""
    client = F1APIClient()

    params = {}
    if driver_number:
        params["driver_number"] = driver_number
    if session_key:
        params["session_key"] = session_key

    data = client.get("drivers", params=params)
    client.close()

    # Check if data is empty or is an error response
    if not data or len(data) == 0:
        print("Warning: No data returned from API")
        return []

    if isinstance(data, dict) and "detail" in data:
        print(f"Warning: API error - {data['detail']}")
        return []

    write_to_parquet(data, "drivers.parquet")
    return data


if __name__ == "__main__":
    drivers_data = get_drivers()

    if drivers_data:
        print("Drivers data fetched and written to parquet successfully.")
    else:
        print("No drivers data to write.")
