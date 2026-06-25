"""DuckCon SQL Queries Module"""


class Queries:
    """SQL Queries"""

    @staticmethod
    def load_ext() -> str:
        return f"""
            INSTALL httpfs;
            LOAD httpfs;
        """


    @staticmethod
    def aws_auth(region: str, credentials: dict) -> str:
        return f"""
            SET s3_region='{region}';
            SET s3_access_key_id='{credentials.access_key}';
            SET s3_secret_access_key='{credentials.secret_key}';
            SET s3_session_token='{credentials.token}';
        """


    @staticmethod
    def fetch_all(table: str) -> str:
        return f"""
            SELECT
                *
            FROM '{table}'
        """


    @staticmethod
    def fetch_all_json(json_file: str) -> str:
        return f"""
            SELECT
                *
            FROM read_json('{json_file}')
        """
