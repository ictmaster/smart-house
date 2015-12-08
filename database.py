import sqlite3
import sys
import json
db_name = 'sqlite_database.db'

def create_database():
        con = sqlite3.connect(db_name)
        c = con.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS data
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT NOT NULL,
            vector TEXT NOT NULL,
            class TEXT NOT NULL
            );
            """)

        c.execute("""CREATE TABLE IF NOT EXISTS summaries
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary TEXT NOT NULL,
            vector_index INTEGER NOT NULL,
            class TEXT NOT NULL
            )
            """)

        con.commit()
        con.close()

def drop_database():
    if input("100%?") != 'yes':
        print("smart choice...")
        sys.exit(0)
    con = sqlite3.connect(db_name)
    c = con.cursor()
    c.execute("DROP TABLE IF EXISTS data")
    c.execute("DROP TABLE IF EXISTS summaries")
    con.commit()
    con.close()

def get_summaries():
    con = sqlite3.connect(db_name)
    c = con.cursor()

    rows = c.execute('select * from summaries;').fetchall()
    d = {}
    for row in rows:
        l = d.get(row[3], [])
        l.append(json.loads(row[1]))
        d[row[3]] = l

    return d
    con.close()

if __name__ == "__main__":
    if 'create' in sys.argv:
        create_database()

    if 'dropdb' in sys.argv and input("YOU SURE ABOUT THIS, you have backup?!") == 'yes':
        drop_database()

    data = get_summaries()
