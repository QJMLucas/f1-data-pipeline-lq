SELECT *
FROM read_parquet('data/raw/*/drivers.parquet', filename=true);