import os
import json
import duckdb

DB_PATH = 'uncommitted/votes.duckdb'
SCHEMA = 'blog_analysis'
TABLE = 'votes'
DATA_PATH = 'uncommitted/votes.jsonl'

CREATE_SCHEMA_SQL = f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};"

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA}.{TABLE} (
    Id         VARCHAR PRIMARY KEY,
    PostId     VARCHAR,
    VoteTypeId VARCHAR,
    CreationDate TIMESTAMP
);
"""

def connect_db():
    return duckdb.connect(DB_PATH)

def ingest_votes(conn, data_path=DATA_PATH):
    cur = conn.cursor()
    cur.execute(CREATE_SCHEMA_SQL)
    cur.execute(CREATE_TABLE_SQL)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Vote data file '{data_path}' not found.")

    # Deduplicate by Id, keep only unique records
    ids_in_db = set(row[0] for row in cur.execute(f"SELECT Id FROM {SCHEMA}.{TABLE};").fetchall())
    with open(data_path, 'r') as f:
        lines = (line.strip() for line in f)
        for line in lines:
            if not line:
                continue
            record = json.loads(line)
            if record['Id'] in ids_in_db:
                continue
            # Insert the record
            cur.execute(
                f"""
                INSERT INTO {SCHEMA}.{TABLE} (Id, PostId, VoteTypeId, CreationDate)
                VALUES (?, ?, ?, ?)
                """,
                [
                    record['Id'],
                    record.get('PostId', ''),
                    record.get('VoteTypeId', ''),
                    record.get('CreationDate', None),
                ]
            )
            ids_in_db.add(record['Id'])

def main():
    conn = connect_db()
    ingest_votes(conn)
    print(f"Ingestion complete. Data inserted into {SCHEMA}.{TABLE}")

if __name__ == "__main__":
    main()