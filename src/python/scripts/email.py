import psycopg2
from config import config

conn = psycopg2.connect(**config())

cur = conn.cursor() 
cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES, users WHERE TABLE_NAME = users.username;")
row = cur.fetchall()

cur2 = conn.cursor() 
cur2.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS, users WHERE TABLE_NAME = users.username;")
row2 = cur2.fetchall()      

while row is not None:
    for i in row:
        i = ' '.join(i)        
        cur.execute(f"SELECT * FROM {i};")
        row = cur.fetchone()    
        print(f"\n{i} - Tuntikirja")

        while row is not None:  
            # cur2.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS, users WHERE TABLE_NAME = users.username;")

            # row2 = cur2.fetchall()                                     
            # rivi2 = '  '.join(map(str,(row2))) 
            # print(rivi2)               

            rivi = ' | '.join(map(str,(row)))
            print(rivi)
            row = cur.fetchone()
