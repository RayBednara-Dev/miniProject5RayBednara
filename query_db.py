"""Quick read-only peek at the golf scores database from the command line.

Usage:
    python query_db.py                       # dump users, rounds, players
    python query_db.py "SELECT * FROM rounds"  # run a custom query
"""
import sqlite3
import sys

DB_PATH = "instance/flaskr.sqlite"


def dump_table(con, table):
    print(f"-- {table} --")
    for row in con.execute(f"SELECT * FROM {table}"):
        print(dict(row))
    print()


def main():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row

    if len(sys.argv) > 1:
        query = sys.argv[1]
        for row in con.execute(query):
            print(dict(row))
    else:
        for table in ("users", "rounds", "players"):
            dump_table(con, table)


if __name__ == "__main__":
    main()
