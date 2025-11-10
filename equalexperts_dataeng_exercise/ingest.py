import sys
from pathlib import Path

import duckdb


def ingest_votes(data_file_path: str) -> None:
    """
    Ingest vote data from a JSONL file into the DuckDB warehouse.

    Creates the blog_analysis schema and votes table if they don't exist.
    Ensures idempotent ingestion - running multiple times won't create duplicates.

    Args:
        data_file_path: Path to the JSONL file containing vote data
    """
    db_path = "warehouse.db"
    conn = duckdb.connect(db_path)

    # Create schema if it doesn't exist
    conn.execute("CREATE SCHEMA IF NOT EXISTS blog_analysis")

    # Create table if it doesn't exist
    # Using INTEGER for Id to serve as primary key for deduplication
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS blog_analysis.votes (
            Id INTEGER PRIMARY KEY,
            PostId INTEGER,
            VoteTypeId INTEGER,
            CreationDate TIMESTAMP
        )
    """
    )

    # Read JSONL file and insert data, ignoring duplicates (based on Id primary key)
    # INSERT OR IGNORE ensures idempotent ingestion
    conn.execute(
        f"""
        INSERT OR IGNORE INTO blog_analysis.votes
        SELECT
            CAST(Id AS INTEGER) as Id,
            CAST(PostId AS INTEGER) as PostId,
            CAST(VoteTypeId AS INTEGER) as VoteTypeId,
            CAST(CreationDate AS TIMESTAMP) as CreationDate
        FROM read_json_auto('{data_file_path}')
    """
    )

    conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python -m equalexperts_dataeng_exercise.ingest <path_to_jsonl_file>"
        )
        sys.exit(1)

    data_file = sys.argv[1]

    if not Path(data_file).exists():
        print(f"Error: File {data_file} does not exist")
        sys.exit(1)

    ingest_votes(data_file)
    print(f"Successfully ingested data from {data_file}")
