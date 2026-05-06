{#non- zero#}
SELECT CASE
  WHEN sum(1) > 0 THEN 'PASS'
  ELSE 'FAIL: No data in laps parquet'
END as test_result
FROM read_parquet('data/raw/laps.parquet');