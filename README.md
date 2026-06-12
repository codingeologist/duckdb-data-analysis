# ducksb-data-analysis

---

Analyse data locally or with AWS S3 partitions with DuckDB

---

## Usage

- create an environment variable `ENV=local` for local operations or `cloud` for AWS operations.
- If not local, create an `AWS_PROFILE` environment variable and authenticate the session with `aws sso login`.
- Run `duck_analysis.py` specifying the `filepath` flag with the path to the data file (or partitioned S3 URI).
- The `queries.py` module has different `SQL` query operations that can be used.
