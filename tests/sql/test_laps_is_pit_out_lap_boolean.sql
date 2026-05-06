{#check data type true or false#}
SELECT CASE
  WHEN count(1) = 0 THEN 'PASS'
  ELSE 'FAIL: Found non-boolean values in is_pit_out_lap'
END as test_result
FROM read_parquet('data/raw/laps.parquet')
WHERE is_pit_out_lap NOT IN (true, false);