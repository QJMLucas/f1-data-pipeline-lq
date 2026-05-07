import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List


def write_to_parquet(
    data: List[Dict[str, Any]],
    filename: str,
    output_dir: str = "data/raw",
    date_start: str = None,
    date_end: str = None,
):
    """Write API response data to parquet file organized by date (YYYYMMDD format).

    Args:
        data: List of dictionaries to write
        filename: Base filename (without extension)
        output_dir: Output directory
        date_start: Optional start date for filename (ISO format, e.g., '2023-01-01')
        date_end: Optional end date for filename (ISO format, e.g., '2023-02-01')
    """
    # Convert API response to DataFrame
    df = pd.DataFrame(data)
    print(df.head())

    # Create date folder (YYYYMMDD)
    today = datetime.now().strftime("%Y%m%d")
    date_output_dir = f"{output_dir}/{today}"
    Path(date_output_dir).mkdir(parents=True, exist_ok=True)

    # Include date range in filename if provided
    if date_start and date_end:
        start_date_str = date_start.split("T")[0]  # Extract YYYY-MM-DD
        end_date_str = date_end.split("T")[0]
        filepath = f"{date_output_dir}/{filename.replace('.parquet', '')}_{start_date_str}_{end_date_str}.parquet"
    else:
        filepath = f"{date_output_dir}/{filename}"

    df.to_parquet(filepath, index=False, engine="pyarrow")
    print(f"Data written to {filepath}")
    return filepath
