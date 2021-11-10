import psycopg2
from data import config as config
import datetime

class Tuntikirja:
    def __init__(self, start_date = 0, end_date = 0, start_time = 0, end_time = 0, project_name = "", definition = ""):
        # self.date = aloituspäivä talteen loppupäivän vertailua varten
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.project_name = project_name
        self.definition = definition
        
    def menu():
        return "Hello world!"

    def set_start_date(self):
        date_entry = input("Anna aloituspäivämäärä muodossa DD/MM/YYYY")
        day, month, year = map(int, date_entry.split('/'))
        self.start_date = datetime.date(year, month, day)
        print(self.start_date)

    def set_start_time():
        pass

    def set_end_date():
        pass

    def set_end_time():
        pass

    def set_project_name(self):
        self.project_name = input("Anna projektin nimi")
        return self.project_name
        
    #     con = None
    # try:
    #     con = psycopg2.connect(**config())
    #     cur = con.cursor()
    #     SQL = "INSERT INTO naamataulu (self.project_name) VALUES (%s);"
    #     val = (input("Anna projektin nimi"))
    #     cur.execute(SQL, val)

    #     print(cur.rowcount, "record inserted.")

    #     con.commit()
    #     cur.close()
    #     con.close()

    # except (Exception, psycopg2.DatabaseError) as error:
    #     print(error)
    # finally:
    #     if con is not None:
    #         con.close()



        pass

    def set_definition():
        pass
    
if __name__ == "__main__":
    #tunnit = Tuntikirja()
    print(Tuntikirja.project())
