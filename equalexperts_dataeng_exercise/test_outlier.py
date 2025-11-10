import duckdb
from ingest import connect_db, ingest_votes, SCHEMA, TABLE
from outliers import VIEW_SQL

# Use dataset from README example
EXAMPLE_DATA = [
    {"Id":"1","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-02T00:00:00.000"},
    {"Id":"2","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"},
    {"Id":"4","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"},
    {"Id":"5","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"},
    {"Id":"6","PostId":"5","VoteTypeId":"3","CreationDate":"2022-01-16T00:00:00.000"},
    {"Id":"7","PostId":"3","VoteTypeId":"2","CreationDate":"2022-01-16T00:00:00.000"},
    {"Id":"8","PostId":"4","VoteTypeId":"2","CreationDate":"2022-01-16T00:00:00.000"},
    {"Id":"9","PostId":"2","VoteTypeId":"2","CreationDate":"2022-01-23T00:00:00.000"},
    {"Id":"10","PostId":"2","VoteTypeId":"2","CreationDate":"2022-01-23T00:00:00.000"},
    {"Id":"11","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-30T00:00:00.000"},
    {"Id":"12","PostId":"5","VoteTypeId":"2","CreationDate":"2022-01-30T00:00:00.000"},
    {"Id":"13","PostId":"8","VoteTypeId":"2","CreationDate":"2022-02-06T00:00:00.000"},
    {"Id":"14","PostId":"13","VoteTypeId":"3","CreationDate":"2022-02-13T00:00:00.000"},
    {"Id":"15","PostId":"13","VoteTypeId":"3","CreationDate":"2022-02-20T00:00:00.000"},
    {"Id":"16","PostId":"11","VoteTypeId":"2","CreationDate":"2022-02-20T00:00:00.000"},
    {"Id":"17","PostId":"3","VoteTypeId":"3","CreationDate":"2022-02-27T00:00:00.000"}
]

def load_example(conn):
    cur = conn.cursor()
    cur.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};")
    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA}.{TABLE} (
        Id         VARCHAR PRIMARY KEY,
        PostId     VARCHAR,
        VoteTypeId VARCHAR,
        CreationDate TIMESTAMP
    );
    """)
    for record in EXAMPLE_DATA:
        cur.execute(f"""INSERT INTO {SCHEMA}.{TABLE} (Id, PostId, VoteTypeId, CreationDate)
            VALUES (?, ?, ?, ?)
            ON CONFLICT DO NOTHING;
        """, [record['Id'], record['PostId'], record['VoteTypeId'], record['CreationDate']])

def test_outlier_view():
    conn = duckdb.connect('uncommitted/test_outlier.duckdb')
    load_example(conn)
    cur = conn.cursor()
    cur.execute(VIEW_SQL)
    result = cur.execute(f"SELECT * FROM {SCHEMA}.outlier_weeks;").fetchall()
    # Expected values from README
    expected = [
        (2022, 0, 1),
        (2022, 1, 3),
        (2022, 2, 3),
        (2022, 5, 1),
        (2022, 6, 1),
        (2022, 8, 1)
    ]
    assert all(row in result for row in expected), "Outlier weeks calculation failed"
    conn.close()
    import os; os.remove('uncommitted/test_outlier.duckdb')

if __name__ == "__main__":
    test_outlier_view()
    print("Outlier weeks calculation test passed")