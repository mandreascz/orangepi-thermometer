import sqlite3

create_stable_statement = """
create table if not exists measurements (
    id integer primary key autoincrement,
    measurement_date timestamp default current_timestamp,
    temperature real not null,
    humidity integer not null
);"""

database = 'measurement_db.db'
if __name__ == '__main__':
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.executescript(create_stable_statement)
        cursor.close()
        conn.close()
        print('Database created ...')
    except Exception as e:
        print('Problems with database creation !!!')
        print(e)
