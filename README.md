## :warning: Please read these instructions carefully and entirely first
* Clone this repository to your local machine.
* Use your IDE of choice to complete the assignment.
* When you have completed the assignment, you need to  push your code to this repository and [mark the assignment as completed by clicking here](https://app.snapcode.review/submission_links/03727d46-14ec-4908-940c-edb609ad0ec9).
* Once you mark it as completed, your access to this repository will be revoked. Please make sure that you have completed the assignment and pushed all code from your local machine to this repository before you click the link.

**Table of Contents**
1. [Before you start](#before-you-start), a brief explanation for the exercise and software prerequisites/setup.  
2. [Tips for what we are looking for](#tips-on-what-were-looking-for) provides clear guidance on solution qualities we value 
3. [The Challenge](#begin-the-two-part-challenge) explains the data engineering code challenge to be tackled.
4. [Follow-up Questions](#follow-up-questions) related to the challenge which you should address  
5. [Your approach and answers to follow-up questions](#your-approach-and-answers-to-follow-up-questions-) is where you should include the answers to the follow-up question and clarify your solution approach any assumptions you have made.

## Before you start
### Why complete this task?

We want to make the interview process as simple and stress-free as possible. That’s why we ask you to complete 
the first stage of the process from the comfort of your own home.

Your submission will help us to learn about your skills and approach. If we think you’re a good fit for our 
network, we’ll use your submission in the next interview stages too.

### About the task

You’ll be creating an ingestion process to ingest files containing vote data. You’ll also create a means to 
query the ingested data to determine outlier weeks.

There’s no time limit for this task, but we expect it to take less than 2 hours.

### Setup Instructions

For instructions on how to set up and run the exercise, please see [SETUP.md](SETUP.md).

### Tips on what we’re looking for


* ✅  **Test coverage**

    Your solution must have good test coverage, including common execution paths.

* ✅  **Self-contained tests**

    Your tests should be self-contained, with no dependency on being run in a specific order.

* ✅  **Simplicity**

    We value simplicity as an architectural virtue and a development practice. Solutions should reflect the difficulty of the assigned task, and shouldn’t be overly complex. We prefer simple, well tested solutions over clever solutions. 

    Please avoid:

   * ❌ unnecessary layers of abstraction
   * ❌ patterns
   * ❌ custom test frameworks
   * ❌ architectural features that aren’t called for
   * ❌ libraries like **pandas** or **polars** or frameworks like **PySpark** or **ballista**
  
     We know that this exercise can be
     solved fairly trivially using these libraries and a Dataframe approach, and we'd encourage appropriate 
     use of these in daily work contexts. But for this small exercise we really 
     want to know more about how you structure, write and test your Python code,
     and want you to show some fluency in SQL -- a **pandas**
     solution won't allow us to see much of that.

* ✅  **Self-explanatory code**

    The solution you produce must speak for itself. Multiple paragraphs explaining the solution is a sign 
    that the code isn’t straightforward enough to understand on its own.
    However, please do explain your non-obvious _choices_ e.g. perhaps why you decided to load
    data a specific way.

* ✅ **Demonstrate fluency with data engineering concepts**
   
   Even though this is a toy exercise, treat DuckDB as you would an OLAP 
   data warehouse. Choose datatypes, data loading methods, optimisations and data models that 
   are suited for resilient analytics processing at scale, not transaction processing.

* ✅ **Dealing with ambiguity**

    If there’s any ambiguity, please add this in a section at the bottom of the README. 
    You should also make a choice to resolve the ambiguity and proceed.

Our review process starts with a very simplistic test set in the `tests/exercise_tests` folder which you should also
check before submission. You can run these with:
```shell
poetry run exercise check-ingestion
poetry run exercise check-outliers
```

Expect these to fail until you have completed the exercise.

You should not change the `tests/exercise-tests` folder and your solution should be able to pass both tests.


## Download the dataset for the exercise
Run the command
```
poetry run exercise fetch-data
```

which will fetch the dataset, uncompress it and place it in `uncommitted/votes.jsonl` for you.
Explore the data to see what values and fields it contains (no need to show how you explored it).

## Begin the two-part challenge
There are two parts to the exercise, and you are expected to complete both. 
A user should be able to execute each task independently of the other. 
For example, ingestion shouldn't cause the outliers query to be executed.

### Part 1: Ingestion
Create a schema called `blog_analysis`.
Create an ingestion process that can be run on demand to ingest files containing vote data. 
You should ensure that data scientists, who will be consumers of the data, do not need to consider 
duplicate records in their queries. The data should be stored in a table called `votes` in the `blog_analysis` schema. 

### Part 2: Outliers calculation
Create a view named `outlier_weeks`  in the `blog_analysis` schema. It will contain the output of a SQL calculation for which weeks are regarded as outliers based on the vote data that was ingested.
The view should contain the year, week number and the number of votes for the week _for only those weeks which are determined to be outliers_, according to the following rule:

NB! If you're viewing this Markdown document in a viewer
where the math isn't rendering, try viewing this README in GitHub on your web browser, or [see this pdf](docs/calculating_outliers.pdf).

> 
> **A week is classified as an outlier when the total votes for the week deviate from the average votes per week for the complete dataset by more than 20%.**</br>  
> For the avoidance of doubt, _please use the following formula_: 
>  
> > Say the mean votes is given by $\bar{x}$ and this specific week's votes is given by $x_i$. 
> > We want to know when $x_i$ differs from $\bar{x}$ by more than $20$%. 
> > When this is true, then the ratio $\frac{x_i}{\bar{x}}$ must be further from $1$ by more than $0.2$, i.e.: </br></br> 
> > $\big|1 - \frac{x_i}{\bar{x}}\big| > 0.2$

The data should be sorted in the view by year and week number, with the earliest week first.

Running `outliers.py` should recreate the view and 
just print the contents of this `outlier_weeks` view to the terminal - don't do any more calculations after creating the view.

## Example

The sample dataset below is included in the test-resources folder and can be used when creating your tests.

Assuming a file is ingested containing the following entries:

```
{"Id":"1","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-02T00:00:00.000"}
{"Id":"2","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"}
{"Id":"4","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"}
{"Id":"5","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"}
{"Id":"6","PostId":"5","VoteTypeId":"3","CreationDate":"2022-01-16T00:00:00.000"}
{"Id":"7","PostId":"3","VoteTypeId":"2","CreationDate":"2022-01-16T00:00:00.000"}
{"Id":"8","PostId":"4","VoteTypeId":"2","CreationDate":"2022-01-16T00:00:00.000"}
{"Id":"9","PostId":"2","VoteTypeId":"2","CreationDate":"2022-01-23T00:00:00.000"}
{"Id":"10","PostId":"2","VoteTypeId":"2","CreationDate":"2022-01-23T00:00:00.000"}
{"Id":"11","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-30T00:00:00.000"}
{"Id":"12","PostId":"5","VoteTypeId":"2","CreationDate":"2022-01-30T00:00:00.000"}
{"Id":"13","PostId":"8","VoteTypeId":"2","CreationDate":"2022-02-06T00:00:00.000"}
{"Id":"14","PostId":"13","VoteTypeId":"3","CreationDate":"2022-02-13T00:00:00.000"}
{"Id":"15","PostId":"13","VoteTypeId":"3","CreationDate":"2022-02-20T00:00:00.000"}
{"Id":"16","PostId":"11","VoteTypeId":"2","CreationDate":"2022-02-20T00:00:00.000"}
{"Id":"17","PostId":"3","VoteTypeId":"3","CreationDate":"2022-02-27T00:00:00.000"}
```

Then the following should be the content of your `outlier_weeks` view:


| Year | WeekNumber | VoteCount |
|------|------------|-----------|
| 2022 | 0          | 1         |
| 2022 | 1          | 3         |
| 2022 | 2          | 3         |
| 2022 | 5          | 1         |
| 2022 | 6          | 1         |
| 2022 | 8          | 1         |

**Note that we strongly encourage you to use this data as a test case to ensure that you have the correct calculation!**

## Follow-up Questions

Please include instructions about your strategy and important decisions you made in the README file. You should also include answers to the following questions, please make sure these are answered without the use AI tools as we would like to understand your thought process:

1. What kind of data quality measures would you apply to your solution in production?
2. What would need to change for the solution scale to work with a 10TB dataset with 5GB new data arriving each day?
3. Please tell us in your modified README about any assumptions you have made in your solution (below).


## How to Run and Test the Solution

### Prerequisites
Ensure you have Python 3.11 and Poetry installed. Alternatively, use the Docker container as described in SETUP.md.

### Step 1: Install Dependencies
```bash
poetry install --with dev
```

### Step 2: Fetch the Dataset
```bash
poetry run exercise fetch-data
```
This downloads and extracts the vote data to `uncommitted/votes.jsonl`.

### Step 3: Run Data Ingestion
```bash
poetry run exercise ingest-data
```
This creates the `blog_analysis` schema and `votes` table, then ingests the data from `uncommitted/votes.jsonl`.

### Step 4: Run Outliers Detection
```bash
poetry run exercise detect-outliers
```
This creates the `outlier_weeks` view and displays the weeks identified as outliers.

### Step 5: Run the Exercise Tests
To verify the implementation passes all required tests:

```bash
# Test ingestion
poetry run exercise check-ingestion

# Test outliers
poetry run exercise check-outliers
```

Both test suites should pass with all tests green.

### Additional Testing Commands

Run your own SQL queries on the database:
```bash
poetry run exercise run-query "SELECT * FROM blog_analysis.votes LIMIT 5"
```

Run all project tests (excluding exercise tests):
```bash
poetry run exercise test
```

Run linting:
```bash
poetry run exercise lint
```

## Your Approach and answers to follow-up questions

### Implementation Approach

**Data Ingestion Strategy:**
I chose a straightforward, SQL-native approach leveraging DuckDB's capabilities:
- **Schema Management:** Used `CREATE SCHEMA IF NOT EXISTS` and `CREATE TABLE IF NOT EXISTS` to ensure idempotent setup
- **Primary Key for Deduplication:** Set `Id` as PRIMARY KEY to naturally enforce uniqueness at the database level
- **INSERT OR IGNORE Pattern:** This ensures idempotent ingestion - running the ingestion multiple times with the same data won't create duplicates
- **DuckDB's read_json_auto():** Utilized DuckDB's native JSON reading capability which automatically infers schema and handles JSONL format efficiently

**Outliers Detection Strategy:**
- **SQL-Based Calculation:** Implemented the entire outlier detection logic in SQL using Common Table Expressions (CTEs) for clarity and performance
- **Week Numbering:** Used `STRFTIME(CreationDate, '%W')` instead of `WEEK()` function because ISO week numbering can place early January dates in week 52/53 of the previous year. The `%W` format gives 0-based week numbers with Monday as the first day, matching the expected output
- **Analytical Approach:** The view calculates mean votes per week across the entire dataset, then filters weeks where the deviation exceeds 20% using the formula `|1 - x_i/x̄| > 0.2`

**Key Design Decisions:**
1. **Idempotency:** Both ingestion and view creation are idempotent - they can be run multiple times safely
2. **Simplicity:** Avoided unnecessary abstractions; kept the code straightforward and readable
3. **Type Safety:** Used explicit CAST operations to ensure correct data types
4. **Database-Centric:** Pushed computation to the database rather than Python, which is more efficient for data processing

### Follow-up Questions

**1. What kind of data quality measures would you apply to your solution in production?**

For production, I would implement:

- **Schema Validation:** Add explicit schema validation before ingestion to ensure all required fields (Id, PostId, VoteTypeId, CreationDate) are present and have valid values
- **Data Type Validation:** Verify that Id and PostId are positive integers, VoteTypeId is within expected range, and CreationDate is a valid timestamp
- **Referential Integrity Checks:** If PostId references another table (posts), add foreign key constraints or validation queries
- **Duplicate Detection:** Beyond the Id-based deduplication, add logging to track when duplicates are encountered (currently silently ignored)
- **Data Range Checks:** Validate that CreationDate falls within expected ranges (e.g., not in the future, not before system start date)
- **Completeness Metrics:** Track the number of records ingested vs. records in source file, alert on significant discrepancies
- **Null Handling:** Explicit handling of NULL values with appropriate defaults or rejection
- **Data Quality Dashboard:** Create views/reports showing ingestion statistics, rejection rates, and data quality metrics over time
- **Audit Trail:** Log each ingestion run with timestamp, source file, records processed, records inserted, and records rejected

**2. What would need to change for the solution to scale to work with a 10TB dataset with 5GB new data arriving each day?**

For scaling to this level:

**Ingestion Changes:**
- **Partitioning:** Partition the votes table by year and month (or week) to improve query performance and enable efficient data pruning
- **Incremental Loading:** Instead of always scanning the entire dataset, track the last processed timestamp and only process new data
- **Batch Processing:** Use DuckDB's parallel processing capabilities or split large files into smaller chunks for parallel ingestion
- **Streaming Approach:** Consider continuous/micro-batch ingestion rather than daily bulk loads if near real-time is needed
- **Compression:** Enable appropriate compression (DuckDB supports this natively) to reduce storage footprint
- **Separate Storage:** Move to a distributed storage system (S3, HDFS) and use DuckDB's ability to query remote files

**Outliers View Changes:**
- **Materialized View or Table:** Convert the view to a materialized table that's updated incrementally rather than recalculated on every query
- **Incremental Calculation:** When new data arrives, only recalculate statistics for affected weeks rather than the entire dataset
- **Pre-aggregation:** Maintain a separate aggregation table (year, week, vote_count) that's updated during ingestion
- **Window-based Mean:** Instead of calculating mean across all data, use a rolling window (e.g., last 12 months) which is more relevant and faster to compute

**Infrastructure:**
- **Distributed Processing:** Consider migrating to a distributed system like Apache Spark or Trino for processing at this scale
- **Separate OLAP System:** DuckDB is excellent for analytics on moderate datasets, but for 10TB+ consider dedicated OLAP databases like ClickHouse, Snowflake, or BigQuery
- **Resource Scaling:** Increase memory and CPU resources; DuckDB can utilize multiple cores effectively
- **Workflow Orchestration:** Use tools like Airflow or Prefect to manage complex ETL pipelines with proper error handling, retries, and monitoring

**3. Assumptions made in the solution:**

- **Data Format:** Assumed the JSONL file contains well-formed JSON objects with string values for all fields (as shown in the example)
- **Id Uniqueness:** Assumed that `Id` is truly unique across all vote records and can serve as the primary key
- **Data Completeness:** Assumed all required fields (Id, PostId, VoteTypeId, CreationDate) are always present in the source data
- **Week Calculation:** Assumed weeks should be calculated using the Monday-based week system (`%W` format) based on the expected output in the README
- **Single Year:** While the implementation handles multiple years, the example data only contains 2022 data
- **No Historical Data:** Assumed we don't need to maintain historical versions of the outlier view - we always want the current calculation
- **No Data Deletion:** The solution doesn't handle deletion of votes; it's an append-only model
- **Time Zone:** Assumed all timestamps are in UTC or a consistent timezone (no timezone conversion needed)
- **Vote Type Filtering:** Made no assumptions about filtering by VoteTypeId - all votes are included in the analysis
- **Database Location:** Assumed `warehouse.db` in the current directory is the correct location (as specified in the tests)
- **Resource Constraints:** Assumed the dataset fits in memory and on a single machine (reasonable for the exercise scope)

## AI Tool Usage

While we encourage the use of AI tools as part of the learning process but to ensure transparency, please provide the following information regarding the use of AI tools in this submission:

1.  **Specific Use Cases:** Describe for what purposes tool was used (e.g., code generation, debugging assistance, query generation etc.).
2.  **Percentage of Code Generated by AI:** Provide an estimate of the percentage of the submitted code that was generated by AI.
3.  **How AI-Generated Code Was Reviewed:** Explain how you reviewed and verified the AI-generated code to ensure its correctness and quality.

Please note, during the technical interview, which will build upon this exercise, we'll focus on your coding abilities and problem-solving skills without the use of AI tools. This will allow us to see your direct approach and thought process.
