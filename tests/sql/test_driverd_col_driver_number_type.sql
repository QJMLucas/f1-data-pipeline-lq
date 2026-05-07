{#check driver number type #}
SELECT CASE
      WHEN typeof(driver_number) = 'BIGINT'
      THEN 'PASS'
      ELSE 'FAIL: driver_number is ' || typeof(driver_number)
END as test_result
FROM read_parquet('data/raw/*/drivers*') LIMIT 1;