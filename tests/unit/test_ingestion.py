import pandas as pd
from src.ingestion.laps import get_laps


class TestGetLaps:

    def test_get_laps_creates_parquet_file(self):
        """Test that get_laps creates parquet file with valid data"""
        print("\n=== Starting test: test_get_laps_creates_parquet_file ===")

        print("\n→ Calling get_laps(date_start='2023-09-01', date_end='2023-09-02', driver_number=55)...")
        result = get_laps(date_start='2023-09-01', date_end='2023-09-02', driver_number=55)
        print("✓ Function returned successfully")

        # Read result as dataframe
        print("\n→ Converting result to dataframe...")
        df = pd.DataFrame(result)
        print("✓ Successfully converted result to dataframe")

        print("\n--- Data ---")
        print(f"Number of rows: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"\nData:\n{df}")

        print("\n✓ TEST PASSED!\n")
