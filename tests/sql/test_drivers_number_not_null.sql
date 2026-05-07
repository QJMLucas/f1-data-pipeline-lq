{#driver number not null#}
SELECT CASE
  WHEN count(1) = 0 THEN 'PASS'
  ELSE 'FAIL'
END as test_result
FROM read_parquet('data/raw/*/drivers*') WHERE driver_number IS NULL;