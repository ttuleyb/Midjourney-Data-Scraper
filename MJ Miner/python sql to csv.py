import pandas as pd
import sqlite3

db_file = "aesthetic.sqlite"

conn = sqlite3.connect(db_file, isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)
db_df = pd.read_sql_query("SELECT * FROM generations", conn)
db_df.to_csv('database.csv', index=False)