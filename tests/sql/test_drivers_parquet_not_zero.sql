{#non- zero#}
SELECT CASE
  WHEN count(1) > 0 THEN 'PASS'
  ELSE 'FAIL: No data in drivers parquet'
END as test_result
FROM read_parquet('data/raw/*/drivers*');