import psycopg2
from config import config
import psycopg2.sql as sql

user="creeppa"

def select_from_table():
    conn = None
    try:
        conn = psycopg2.connect(**config())
        cur = conn.cursor()   
        cur.execute(
            sql.SQL("SELECT * FROM {}").format(sql.Identifier(user)))
        row = cur.fetchone()

        field_names = [i[0]
        for i in cur.description]
        print(f"{field_names}")

        while row is not None:
            print(f"{row}")
            row = cur.fetchone()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()  

if __name__ == "__main__":
    select_from_table()