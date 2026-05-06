{#check if any null data in sessionid#}
SELECT CASE
  WHEN count(1) = 0 THEN 'PASS'
  ELSE 'FAIL: Found ' || sum(1) || ' null session_keys'
END as test_result
FROM read_parquet('data/raw/laps.parquet') WHERE session_key IS NULL;