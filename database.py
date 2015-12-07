import sqlite3
db_name = 'sqlite_database.db'

def recreate_database():
    con = sqlite3.connect(db_name)
    c = con.cursor()
    c.execute("DROP TABLE IF EXISTS data")

    c.execute("""CREATE TABLE data
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value TEXT NOT NULL,
        vector TEXT NOT NULL,
        class TEXT NOT NULL
        );
        """)
    con.commit()
    con.close()


if __name__ == "__main__":
    recreate_database()
