from datetime import datetime

class Tuntikirja:
    def __init__(self):
        #self.date = aloituspäivä talteen loppupäivän vertailua varten
        pass
        
    def menu():
        return "Hello world!"

    def start_date():
        pass

    def start_time():
        pass

    def end_date():
        date2 = input("Anna työpäivän lopetuspäivämäärä muodossa yyyy/mm/dd")
        date2 = date.datetime(yyyy, mm, dd)
        if date1 > date2:
            valinta = input("Lopetuspäivämäärä on ennen aloituspäivämäärää, halaisitko muuttaa sen? Valitse k tai e")
            if valinta == 'k':
                return start_date()
            else:
                continue
            continue
        con = None 
        try: 
            con = psycopg2.connect(**config()) 
            cur = con.cursor() 
            SQL = "INSERT INTO self.table (date2)  VALUES (%s) ;" 
            cur.execute(SQL,(enddate))
            cursor = con.cursor()
            con.commit()
            count = cursor.rowcount

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()

    def end_time(time2):

        con = None 
        try: 
            con = psycopg2.connect(**config()) 
            cur = con.cursor() 
            SQL = "INSERT INTO self.table (time2)  VALUES (%s) ;" 
            cur.execute(SQL,(time2))
            cursor = con.cursor()
            con.commit()
            count = cursor.rowcount

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()

            first_date = datetime.date(2020, 12, 16)
            second_date = datetime.date(2015, 12, 16)

result = first_date < second_date
print(result)
            #palaa start dateen! Printtaa et ootko varma?

    def project():
        pass

    def input():
        pass
    
if __name__ == "__main__":
    #tunnit = Tuntikirja()
    print(Tuntikirja.menu())
