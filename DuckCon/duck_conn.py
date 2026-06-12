"""DuckCon Data Connection Module"""
import os
import boto3
import duckdb
from DuckCon.queries import Queries
from botocore.exceptions import NoCredentialsError, ClientError


class DBAuth:
    """Authenticate DB Connection"""

    def __init__(self) -> None:

        self.env = os.getenv("ENV", "local")
        self._conn = None
        if self.env != "local":
            self.profile = os.getenv("AWS_PROFILE", "")
            self._session = boto3.Session(profile_name=self.profile)
            self._credentials = self._session.get_credentials()
        self._setup_duckdb()


    @property
    def session(self) -> boto3.Session():
        """Create AWS Session"""

        if self._session is None:
            try:
                self._session = boto3.Session(profile_name=self.profile) if self.profile else boto3.Session()
            except Exception as ex:
                raise ClientError(f"Failed to create AWS session: {ex}. Check AWS_PROFILE env var")
        return self._session


    @property
    def credentials(self):
        """Authenticate AWS session and return credentials"""

        if self._credentials is None:
            try:
                self._credentials = self.session.get_credentials()
            except NoCredentialsError:
                raise ClientError(f"AWS Credentials not found. Set AWS_PROFILE and login with aws sso login.")
            except ClientError as ex:
                raise ClientError(f"AWS access denied: {ex}. Check profile permissions.")
        return self._credentials


    @property
    def conn(self):
        """DuckDB Connection"""
        
        if self._conn is None:
            self._conn = duckdb.connect()
            self._setup_duckdb()
        return self._conn


    def _setup_duckdb(self):
        """Setup DuckDB"""
        
        # if runtime is AWS lambda instance
        if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
            self.conn.query("SET home_directory='/tmp';")
        queries = Queries()
        if self.env != "local":
            self.conn.query(queries.load_ext())
            self.conn.query(queries.aws_auth(
                region=self.session.region_name,
                credentials=self.credentials
            ))


    def _show_dataframe(self, data: duckdb.DuckDBPyRelation) -> None:
        """show the dataframe results"""

        data.show()


    def _to_records(self, data: duckdb.DuckDBPyRelation) -> list:
        """DuckDB relation to a list of dict records"""
        
        return [dict(zip(data.columns, row)) for row in data.fetchall()]


    def query_data(self, path: str) -> list:
        """
        Query data by providing a filepath or a partitioned S3 uri
        s3_uri partition format: s3://[BUCKET_NAME]/[PREFIX]/*/*/*/*/*/*/*.json (for each datetime and filetype)
        user queries.fetch_all() for csv files and fetch_all_json() if specified filepath is for json partitions
        """

        queries = Queries()
        df = self.conn.query(queries.fetch_all(table=path))
        self._show_dataframe(data=df)

        return self._to_records(data=df)
