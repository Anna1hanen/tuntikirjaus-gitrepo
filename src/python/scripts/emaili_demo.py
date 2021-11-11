import psycopg2
from config import config


conn = psycopg2.connect(**config())
cur = conn.cursor() 
cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES, users WHERE TABLE_NAME = users.username;")
row = cur.fetchall()
while row is not None:
    for i in row:
        i = ' '.join(i)        
        cur.execute(f"SELECT * FROM {i};")
        row = cur.fetchone()    
        print(f"\n{i} - Tuntikirja")
        while row is not None:  
            rivi = ' | '.join(map(str,(row)))
            print(rivi)
            row = cur.fetchone()
