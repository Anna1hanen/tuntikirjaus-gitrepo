from queries import connect as connect
import sys
import psycopg2

def name(table):
    pass

def start(startdate):
    #sys.arv[1] = input("Anna aloituspäivämäärä muodossa DD/MM/YYYY: ")
            #sys.arv[1] = Day, month, year = map(int, date.split('/'))  
            #sys.arv[1] = datetime.date(day, month, year) 
    con = None 
    try: 
        con = psycopg2.connect(**config()) 
        cur = con.cursor() 
        SQL = "INSERT INTO sys.argv[5] (startdate)  VALUES (%s) ;" 
        cur.execute(SQL,(startdate))
        cursor = con.cursor()
        con.commit()
        count = cursor.rowcount #tarvitaanko?

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
        return

def starttime(starttime):
    #sys.arv[2] = input("Anna aloituskellonaika muodossa: ")
    pass

def end(enddate):
    #sys.arv[3] = input("Anna lopetuspäivämäärä: ")

def endtime(endtime):
    pass
    #tänne 

if __name__ == "__main__":
        
            Day, month, year = map(int, date.split('/'))  
            date2 = datetime.date(day, month, year)
            try:
                if date2.day > date1.day:
                    continue
                else:
                    print("Loppupäivä ei voi olla ennen alkupäivää")
                    #miten pääsi aloittamaan alusta?
        sys.arv[4] = input("Anna lopetuskellonaika: ")
            #tähän sama kuin aiemmassa mutta kellonajoilla
        sys.arv[5] = input("Anna projektin nimi: ")
        start(startdate=sys.arv[1], starttime=sys.arv[2])
        end(enddate=sys.arv[3], endtime=sys.arv[4])
        name(table=sys.arv[5])