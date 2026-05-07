# F1 Data Pipeline

A Python-based ETL pipeline for ingesting and processing Formula 1 data.

## Prerequisites

- Python 3.11 or higher

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd f1-data-pipeline-lq
```

### 2. Create and activate a virtual environment
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Pipeline

### Run drivers module
```bash
python -m src.ingestion.drivers
```

### Run laps module
```bash
python -m src.ingestion.laps
```
Note: Laps is set to incremental load by default, fetching data from 2023 onwards. The laps endpoint requires at least 1 parameter.

### Read from parquet file
Change the SQL file path to check different data:

**Read drivers**
```bash
python -c "import duckdb; duckdb.sql(open('tests/manual_tests/read_drivers.sql').read()).show()"
```

**Read laps**
```bash
python -c "import duckdb; duckdb.sql(open('tests/manual_tests/read_laps.sql').read()).show()"
```

### Run Dagster
```bash
dagster dev
```

## Linting and Formatting

### Check code with ruff
```bash
ruff check .
ruff format . --check
```

### Auto-fix issues
```bash
ruff format .
ruff check . --fix
```

## Testing

### Run SQL tests
```bash
pytest tests/test_sql.py -v
```

### Run unit tests
```bash
pytest tests/unit/test_api_client.py -v -s
pytest tests/unit/test_ingestion.py -v -s
pytest tests/unit/test_storage.py -v -s
```

## Monitoring & Troubleshooting

### Monitor pipeline health

Check pipeline health locally:
- Files appear under `data/raw/YYYYMMDD/` after running the laps or drivers module
- Use the SQL files in `tests/manual_tests/` to verify data was exported successfully (feel free to modify the cscript and query:
  - `read_drivers.sql` — Query drivers data
  - `read_laps.sql` — Query laps data
- Run pipeline in Dagster UI (`dagster dev`) to see job status and logs

### Handle failed runs

**Current behavior:**
- The pipeline includes retry logic with exponential backoff for transient failures
- Laps module uses incremental load by default (fetches from yesterday's max date)

**To test backfill mode:**
1. Run backfill: `python -m src.ingestion.laps --mode backfill` (fetches from 2023 onwards)
2. Rename the output folder to yesterday's date (e.g., if today is 2026-05-08, rename to `20260507`)
3. Modify `laps.py` to call `get_laps()` instead of `get_laps(mode='backfill')`
4. This simulates a second run where yesterday's data exists and incremental load starts from yesterday's max date

test