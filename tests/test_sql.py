import pytest
import duckdb
import re
from pathlib import Path


def clean_query(query):
    """Remove {# #} comments and clean query"""
    query = re.sub(r'\{.*?\}', '', query, flags=re.DOTALL)
    return query.strip()


# Discover all SQL test files
sql_dir = Path(__file__).parent / 'sql'
sql_files = sorted(sql_dir.glob('test_*.sql'))


@pytest.mark.parametrize('sql_file', sql_files, ids=lambda f: f.name)
def test_sql(sql_file):
    """Run SQL test from file"""
    print(f"\n--- Running {sql_file.name} ---")

    with open(sql_file, 'r') as f:
        content = f.read()

    # Get repo root (2 directories up from tests/)
    repo_root = Path(__file__).parent.parent

    # Split by semicolon to handle multiple queries per file
    queries = content.split(';')

    for i, query in enumerate(queries, 1):
        query = clean_query(query)
        if not query:
            continue

        # Replace relative paths with absolute paths
        query = query.replace(
            "read_parquet('data/raw/",
            f"read_parquet('{repo_root}/data/raw/"
        )

        print(f"Query {i}:")
        result = duckdb.query(query).to_df()
        print(f"  Result: {result.to_string()}")

        # Check if result contains PASS or FAIL
        result_val = str(result.iloc[0, 0])
        if 'PASS' in result_val:
            print("  ✓ PASS")
        else:
            assert False, f"Query {i} failed: {result_val}"
