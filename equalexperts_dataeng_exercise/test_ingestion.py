import duckdb
import os
import json
from ingest import ingest_votes, connect_db, SCHEMA, TABLE

TEST_DB = 'uncommitted/test_votes.duckdb'
TEST_DATA = [
    {"Id":"1","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-02T00:00:00.000"},
    {"Id":"2","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"},
    {"Id":"2","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"},  # Duplicate
    {"Id":"3","PostId":"5","VoteTypeId":"3","CreationDate":"2022-01-16T00:00:00.000"},
]

def setup_test_jsonl():
    path = 'uncommitted/test_votes.jsonl'
    with open(path, 'w') as f:
        for record in TEST_DATA:
            json.dump(record, f)
            f.write('\n')
    return path

def test_ingest_deduplication():
    test_path = setup_test_jsonl()
    conn = duckdb.connect(TEST_DB)
    ingest_votes(conn, test_path)
    rows = conn.cursor().execute(f"SELECT COUNT(*) FROM {SCHEMA}.{TABLE};").fetchone()
    assert rows[0] == 3, "Should ingest only unique ids"
    os.remove(test_path)
    os.remove(TEST_DB)

if __name__ == "__main__":
    test_ingest_deduplication()
    print("Ingestion deduplication test passed")