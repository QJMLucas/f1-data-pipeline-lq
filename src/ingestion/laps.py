import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .api_client import F1APIClient
from ..storage.parquet_writer import write_to_parquet


def get_last_loaded_date(output_dir: str = "data/raw") -> str | None:
    """Get the maximum date_start from laps.parquet in yesterday's folder for incremental load."""
    output_path = Path(output_dir)
    if not output_path.exists():
        return None

    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    yesterday_folder = output_path / yesterday

    if not yesterday_folder.exists():
        return None

    filepath = yesterday_folder / "laps.parquet"

    if not filepath.exists():
        return None

    df = pd.read_parquet(filepath)
    if df.empty or "date_start" not in df.columns:
        return None

    max_date = df["date_start"].max()
    print("max_date is " + str(max_date))

    if pd.notna(max_date):
        return str(max_date)
    return None


def _fetch_laps_single_period(
    date_start,
    date_end,
    is_final=False,
    session_key=None,
    driver_number=None,
    lap_number=None,
):
    """Helper function to fetch laps for a single date range.

    Args:
        is_final: If True, name the file as laps.parquet (for final/current month). Otherwise use date range format.
    """
    client = F1APIClient()

    endpoint = "laps"
    query_parts = []

    if date_start:
        query_parts.append(f"date_start>={date_start}")
    if date_end:
        query_parts.append(f"date_start<{date_end}")
    if session_key:
        query_parts.append(f"session_key={session_key}")
    if driver_number:
        query_parts.append(f"driver_number={driver_number}")
    if lap_number:
        query_parts.append(f"lap_number={lap_number}")

    if query_parts:
        endpoint = endpoint + "?" + "&".join(query_parts)

    data = client.get(endpoint)
    client.close()

    if not data or len(data) == 0:
        print(f"Warning: No data returned for {date_start} to {date_end}")
        return []

    if isinstance(data, dict) and "detail" in data:
        print(f"Warning: API error - {data['detail']}")
        return []

    if is_final:
        write_to_parquet(data, "laps.parquet")
    else:
        write_to_parquet(data, "laps.parquet", date_start=date_start, date_end=date_end)
    return data


def get_laps(
    mode="incremental",
    session_key=None,
    driver_number=None,
    lap_number=None,
    date_start=None,
    date_end=None,
):
    """Fetch laps data from OpenF1 API and write to parquet.

    Args:
        mode: 'incremental' (fetch new data since last load) or 'backfill' (fetch month by month from 2023-01-01)
        session_key: Filter by session key
        driver_number: Filter by driver number
        lap_number: Filter by lap number
        date_start: Lower bound - fetch laps >= this date (ISO format). Used for incremental mode if provided.
        date_end: Upper bound - fetch laps < this date (ISO format).
    """
    if mode == "backfill":
        current_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
        end_date = datetime.now()

        while current_date < end_date:
            next_month = current_date + relativedelta(months=1)
            period_start = current_date.strftime("%Y-%m-%dT00:00:00.000000+00:00")
            period_end = next_month.strftime("%Y-%m-%dT00:00:00.000000+00:00")

            # Check if this is the final (current) month
            is_final = next_month > end_date

            print(f"Backfilling {period_start} to {period_end}")
            _fetch_laps_single_period(
                period_start,
                period_end,
                is_final=is_final,
                session_key=session_key,
                driver_number=driver_number,
                lap_number=lap_number,
            )
            current_date = next_month

    elif mode == "incremental":
        if date_start is None:
            date_start = get_last_loaded_date()

        if date_end is None:
            date_end = (
                datetime.utcnow()
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
            )

        print("date_start >= " + str(date_start), "end_time < " + str(date_end))
        _fetch_laps_single_period(
            date_start,
            date_end,
            is_final=True,
            session_key=session_key,
            driver_number=driver_number,
            lap_number=lap_number,
        )


if __name__ == "__main__":
    get_laps(mode="backfill")
    # get_laps()
