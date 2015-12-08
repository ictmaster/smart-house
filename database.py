import sqlite3
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

        con.commit()
        con.close()


def drop_database():
    con = sqlite3.connect(db_name)
    c = con.cursor()
    c.execute("DROP TABLE IF EXISTS data")
    c.execute("DROP TABLE IF EXISTS summaries")
    con.commit()
    con.close()

if __name__ == "__main__":
    pass
