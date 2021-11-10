
import psycopg2
from config import config
from datetime import datetime, date, time


class Tuntikirja:
    def __init__(self, start_date = 0, end_date = 0, start_time = 0, end_time = 0, project_name = "", definition = ""):

        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.project_name = project_name
        self.definition = definition

    def set_start_date(self):
        while True:
            try:
                date_entry = input("Anna aloituspäivämäärä muodossa DD/MM/YYYY\n>")
                day, month, year = map(int, date_entry.split('/'))
                self.start_date = datetime.date(year, month, day)
                return self.start_date
            except Exception as e:
                print(f"Virheellinen syöte, {e}")
                continue

    def set_start_time(self):
        while True:
            try:
                date_entry = input("Anna aloitusaika muodossa HH:MM\n>")
                hour, minute = map(int, date_entry.split(':'))
                self.start_time = datetime.time(hour, minute)
                return self.start_time
            except Exception as e:
                print(f"Virheellinen syöte, {e}")

    def set_end_date(self):
        enddate_entry = input("Anna aloituspäivämäärä muodossa DD/MM/YYYY")
        day, month, year = map(int, enddate_entry.split('/'))
        self.end_date = datetime.date(year, month, day)
        if self.start_date > self.end_date:
            valinta = input(f"Lopetuspäivämäärä ({self.end_date}) on ennen aloituspäivämäärää ({self.start_date}), haluaisitko muuttaa sen? Valitse k tai e")
            if valinta == 'k' or valinta =='K':
                return self.start_date()
            else:
                return self.end_date

    def set_end_time(self):
        endtime_entry = input("Anna lopetusaika muodossa HH:MM")
        self.end_time = datetime.datetime.strptime(endtime_entry, '%H:%M').time()
        end_time_and_end_date = date.self.end_date + time.self.end_time
        start_time_and_start_date = date.self.start_date + time.self.end_time
        if start_time_and_start_date > end_time_and_end_date:
            valinta = input(f"Työn lopetusajankohta ({self.end_time}) ei voi ennen aloitusajankohtaa ({self.start_time}). Haluatko muuttaa aloitusajankohtaa? Vastaa k, jos haluat")
            if valinta == 'k' or valinta == 'K':
                return set_start_date()
        
            return self.end_time

        
    def set_project_name(self):
        self.project_name = input("Anna projektin nimi: ")
        return self.project_name

    
    def set_definition(self):
        self.definition = input("Anna työskentelyn sisältö: ")
        return self.definition

    def insert_to_database(self):
        con = None
        try:
            con = psycopg2.connect(**config())
            cur = con.cursor()
            SQL = "INSERT INTO elina (project_name, definition) VALUES (%s, %s);"
            val = (self.project_name, self.definition)
            cur.execute(SQL, val)         
            print(cur.rowcount, "record inserted.")

            con.commit()
            cur.close()
            con.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if con is not None:
                con.close()       


if __name__ == "__main__":

    def menu():
        menu_commands = "1: Lisää uusi tuntikirja \n" \
                        "2: Katso kuluneen viikon tuntikirjaukset \n" \
                        "3: Poistu\n>"
        while True:
            try:
                command = int(input(menu_commands))
                if command == 1:
                    # tee uusi tuntikirja
                    make_new_worklog()
                elif command == 2:
                    # katso tuntikirjaukset
                    pass
                elif command == 3:
                    # lopettaa ohjelman
                    break
                else:
                    print("Virheellinen syöte")
            except Exception as e:
                print(f"Virheellinen syöte, {e}")

    def make_new_worklog():
        tuntikirja = Tuntikirja()
        tuntikirja.set_project_name()
        tuntikirja.set_definition()
        tuntikirja.insert_to_database()
    
    menu()