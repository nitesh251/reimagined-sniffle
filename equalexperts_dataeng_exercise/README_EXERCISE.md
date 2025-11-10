## Implementation Approach

This repo demonstrates two main functionalities:

1. **Data Ingestion**
    - JSONL vote records are loaded into a DuckDB database in the `blog_analysis.votes` table.
    - Duplicates are ignored by the unique `Id` (primary key).
    - All required fields (Id, PostId, VoteTypeId, CreationDate) are stored.
    - The ingestion script can be rerun safely (idempotent).

2. **Outlier Calculation**
    - Outliers are weeks whose vote count deviates >20% from the mean votes per week.
    - This is implemented as a DuckDB SQL view (`blog_analysis.outlier_weeks`).
    - Output is sorted by year and week, matching the format in the example.

### Assumptions

- `CreationDate` is always present and valid in the input.
- The DuckDB instance is stored at `uncommitted/votes.duckdb`.
- There are no duplicate Ids in the vote input data (enforced by ingestion code).

### Data Quality Measures for Production

- Input validation for missing fields and timestamp parsing.
- Logged errors for corrupt records.
- Additional uniqueness and integrity checks.
- Automated incremental ingestion for new data, with error backoff and reporting.

### Scaling for Large Data Volumes

To scale to 10TB+ and daily 5GB increments:
- Move DuckDB to a cloud/object-storage, or transition to scalable OLAP solutions (e.g. Snowflake, BigQuery).
- Use partitioned tables or data lakes for efficient weekly queries.
- Ingestion with batching and parallel processing.
- Use strong typed schemas for reliability.
- Migrate outlier calculation to run as scheduled jobs/views (not on user query).

### AI Tool Usage

1. Some code, comments, and structure were generated with GitHub Copilot and reviewed line-by-line.
2. Less than 30% of the code was suggested by Copilot; final code, schema, and SQL logic were hand-adjusted to meet clarity and real-world standards.
3. Every Copilot suggestion was checked for correctness, and SQL was manually tested with the sample dataset.

---

Feel free to inspect the SQL and Python scripts for further details.