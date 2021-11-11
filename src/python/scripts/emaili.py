import psycopg2
from config import config
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login("elinaylk", "salasananionsalaisuus")

def viesti():
    conn = psycopg2.connect(**config())
    cur = conn.cursor() 
    cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES, users WHERE TABLE_NAME = users.username;")
    row = cur.fetchall()
    viesti = open("viesti.txt", "a")
    while row is not None:
        for i in row:
            i = ' '.join(i)        
            cur.execute(f"SELECT * FROM {i};")
            row = cur.fetchone()    
            viesti.write(f"\n{i} - Tuntikirja")
            while row is not None:  
                rivi = ' | '.join(map(str,(row)))
                viesti.write(rivi)
                row = cur.fetchone()
    return viesti

if __name__ == "__main__":
    msg = viesti()
    server.sendmail("elinaylk", "creep-89@hotmail.com", (msg))