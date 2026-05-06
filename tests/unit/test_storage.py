import pytest
import os
import pandas as pd
from pathlib import Path
from src.storage.parquet_writer import write_to_parquet


class TestWriteToParquet:

    def test_write_to_parquet_creates_file(self):
        """Test that data is written to parquet file"""
        print("\n=== Starting test: test_write_to_parquet_creates_file ===")

        data = [{'driver_number': 1, 'name': 'Max'}, {'driver_number': 2, 'name': 'Charles'}]
        filename = 'test_driver_write.parquet'

        print(f"✓ Test data prepared: {data}")

        # Call write_to_parquet
        print(f"\n→ Calling write_to_parquet(data, '{filename}')...")
        filepath = write_to_parquet(data, filename)

        print(f"✓ Function returned filepath: {filepath}")

        # Verify file exists
        print(f"\n→ Verifying file exists...")
        assert os.path.exists(filepath), f"File {filepath} was not created"
        print(f"✓ File exists at {filepath}")


        # Verify it's valid parquet and readable
        print(f"\n→ Reading parquet file...")
        df = pd.read_parquet(filepath)
        print(f"✓ Successfully read parquet file")

        # Verify data
        print(f"\n--- Data Verification ---")
        print(f"Number of rows: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Data:\n{df}")

        assert len(df) == 2, f"Expected 2 rows, got {len(df)}"
        print(f"✓ Correct number of rows (2)")

        assert 'driver_number' in df.columns, "Column 'driver_number' not found"
        print(f"✓ Column 'driver_number' exists")

        assert 'name' in df.columns, "Column 'name' not found"
        print(f"✓ Column 'name' exists")

        assert df.iloc[0]['driver_number'] == 1, "First row driver_number incorrect"
        print(f"✓ First row data correct: driver_number=1")

        assert df.iloc[1]['driver_number'] == 2, "Second row driver_number incorrect"
        print(f"✓ Second row data correct: driver_number=2")

        # Cleanup
        print(f"\n→ Cleaning up test file...")
        os.remove(filepath)
        print(f"✓ Test file removed")

        print(f"\n✓ TEST PASSED!\n")
