"""DuckDB Data Analysis Module"""
from argparse import ArgumentParser
from DuckCon.duck_conn import DBAuth


def main():
    
    
    parser = ArgumentParser(
        prog="DuckDB Analysis Module",
        description="Analyse partitioned S3 data or files locally"
    )

    parser.add_argument("-f", "--filepath", help="filepath or partitioned S3 URI to query")
    args = parser.parse_args()

    db = DBAuth()
    db.conn
    
    if args.filepath:
        data = db.query_data(path=args.filepath)
    else:
        print("filepath or S3_uri not specified!")


if __name__ == "__main__":

    main()
