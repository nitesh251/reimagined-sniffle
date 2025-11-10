import duckdb

DB_PATH = 'uncommitted/votes.duckdb'
SCHEMA = 'blog_analysis'
TABLE = 'votes'
VIEW = 'outlier_weeks'

def connect_db():
    return duckdb.connect(DB_PATH)

VIEW_SQL = f"""
CREATE OR REPLACE VIEW {SCHEMA}.{VIEW} AS
WITH weekly_votes AS (
    SELECT
        EXTRACT('year' FROM CreationDate) AS year,
        EXTRACT('week' FROM CreationDate) AS week_number,
        COUNT(*) AS vote_count
    FROM {SCHEMA}.{TABLE}
    GROUP BY year, week_number
),
mean_votes AS (
    SELECT AVG(vote_count) AS mean_vote
    FROM weekly_votes
)
SELECT
    w.year,
    w.week_number,
    w.vote_count
FROM weekly_votes w, mean_votes m
WHERE ABS(1 - (w.vote_count / m.mean_vote)) > 0.2
ORDER BY w.year, w.week_number ASC;
"""

def print_outliers(conn):
    cur = conn.cursor()
    cur.execute(VIEW_SQL)
    result = cur.execute(f"SELECT * FROM {SCHEMA}.{VIEW};").fetchall()
    if not result:
        print("No outlier weeks found.")
        return
    print(f"{'Year':<6} {'WeekNumber':<11} {'VoteCount':<10}")
    print("-" * 30)
    for row in result:
        print(f"{int(row[0]):<6} {int(row[1]):<11} {int(row[2]):<10}")

def main():
    conn = connect_db()
    print_outliers(conn)

if __name__ == "__main__":
    main()