import duckdb


def create_outlier_weeks_view() -> None:
    """
    Create the outlier_weeks view in the blog_analysis schema.
    
    A week is classified as an outlier when the total votes for the week
    deviate from the average votes per week by more than 20%.
    
    Formula: |1 - x_i/x̄| > 0.2
    where x̄ is the mean votes per week and x_i is the votes for a specific week.
    """
    db_path = "warehouse.db"
    conn = duckdb.connect(db_path)
    
    # Drop view if it exists to recreate it
    conn.execute("DROP VIEW IF EXISTS blog_analysis.outlier_weeks")
    
    # Create the outlier_weeks view
    conn.execute("""
        CREATE VIEW blog_analysis.outlier_weeks AS
        WITH weekly_votes AS (
            SELECT 
                YEAR(CreationDate) AS Year,
                CAST(STRFTIME(CreationDate, '%W') AS INTEGER) AS WeekNumber,
                COUNT(*) AS VoteCount
            FROM blog_analysis.votes
            GROUP BY YEAR(CreationDate), CAST(STRFTIME(CreationDate, '%W') AS INTEGER)
        ),
        avg_votes AS (
            SELECT AVG(VoteCount) AS mean_votes
            FROM weekly_votes
        )
        SELECT 
            wv.Year,
            wv.WeekNumber,
            wv.VoteCount
        FROM weekly_votes wv
        CROSS JOIN avg_votes av
        WHERE ABS(1.0 - wv.VoteCount / av.mean_votes) > 0.2
        ORDER BY wv.Year, wv.WeekNumber
    """)
    
    conn.close()


def display_outlier_weeks() -> None:
    """Display the contents of the outlier_weeks view."""
    db_path = "warehouse.db"
    conn = duckdb.connect(db_path, read_only=True)
    
    result = conn.sql("SELECT * FROM blog_analysis.outlier_weeks")
    result.show()
    
    conn.close()


if __name__ == "__main__":
    create_outlier_weeks_view()
    display_outlier_weeks()
