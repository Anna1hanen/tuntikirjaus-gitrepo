import datetime
from config import config
import psycopg2
import psycopg2.sql as sql

user = "Elina"

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
        while True:
            try:
                enddate_entry = input("Anna lopetuspäivä muodossa DD/MM/YYYY\n>")
                day, month, year = map(int, enddate_entry.split('/'))
                self.end_date = datetime.date(year, month, day)
                if self.start_date > self.end_date:
                    valinta = int(input(f"Lopetuspäivämäärä ({self.end_date}) on ennen aloituspäivämäärää ({self.start_date}), haluaisitko muuttaa aloituspäivän? \nValitse 1, jos haluat muuttaa aloituspäivän. \nValitse 2, jos haluat muuttaa lopetuspäivän. \n"))
                    if valinta == 1:
                        self.set_start_date()
                        return self.end_date
                    elif valinta ==2:
                        self.set_end_date()
                return self.end_date
                    

            except Exception as e:
                print(f"Virheellinen syöte, {e}")
                continue

             
    def set_end_time(self):
        while True:
            try:
                endtime_entry = input("Anna lopetusaika muodossa HH:MM\n>")
                hour, minute = map(int, endtime_entry.split(':'))
                self.end_time = datetime.time(hour, minute)
                if self.start_date > self.end_date:
                    valinta = int(input(f"Työn lopetusajankohta ({self.end_time}) ei voi ennen aloitusajankohtaa ({self.start_time}). Haluatko muuttaa aloitusajankohtaa? Vastaa 1, jos haluat.\n>"))
                    if valinta == 1:
                        self.set_start_date()
                elif self.start_date < self.end_date:
                    return self.end_time
                elif self.start_date == self.end_date:
                    if self.end_time <= self.start_time:
                        valinta = int(input(f"Antamasi lopetuskellonaika {self.end_time} on joko sama tai ennen aloitusajankohtaa {self.start_time}.\n Jos haluat vaihtaa alkupäivän: valitse 1.\n Jos haluat vaihtaa alkuajan: valitse 2.\n Jos haluat vaihtaa lopetuspäivän: valitse 3.\n Jos haluat vaihtaa lopetuskellonajan, valitse 4\n>"))
                        if valinta == 1:
                            self.set_start_time()
                        elif valinta == 2:
                            self.set_start_time()
                        elif valinta == 3:
                            self.set_end_date()
                        elif valinta == 4:
                            self.set_end_time()
                        else:
                            print("Valitse numero 1-4 väliltä.")
                    elif self.end_time > self.start_time:
                        return self.end_time
            except Exception as e:
                print(f"Virheellinen syöte, {e}")        
  
    def set_project_name(self):
        self.project_name = input("Anna projektin nimi: \n>")
        return self.project_name

    
    def set_definition(self):
        self.definition = input("Anna työskentelyn sisältö: \n>")
        return self.definition


    def __str__(self):
        return f"Aloitus päivä: {self.start_date}\n" \
               f"Aloitus aika: {self.start_time}\n" \
               f"Lopetus päivä: {self.end_date}\n" \
               f"Lopetus aika: {self.end_time}\n" \
               f"Projektin nimi: {self.project_name}\n" \
               f"Selite: {self.definition}"


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
            # tuli virhe jossain päin koodia

            # raise tarkempaa testausta varten
            raise e

            # raaka errorin printti
            # print(f"Virheellinen syöte, {e}")

            # käyttäjäystävällisempi printti?
            # print("Voihan juukeli jokin meni pieleen")


def make_new_worklog():
    tuntikirja = Tuntikirja()
    tuntikirja.set_start_date()
    tuntikirja.set_start_time()
    tuntikirja.set_end_date()
    tuntikirja.set_end_time()
    tuntikirja.set_project_name()
    tuntikirja.set_definition()
    print(f"\n{tuntikirja}\n")

    insert_to_database(tuntikirja)

# Laitetaan data databaseen
def insert_to_database(tuntikirja):
    conn = None
    try:        
        conn = psycopg2.connect(**config())
        cur = conn.cursor()
        # tarkistetaan onko taulu jo olemassa, jos on; pass
        if check_if_table_exists(conn, cur):
            pass
        # jos ei; luodaan uusi taulu
        else:
            cur.execute(
                sql.SQL("""CREATE TABLE {}(
                    id              serial primary key,
                    start_date      varchar(255) NOT NULL,
                    start_time      varchar(255) NOT NULL,
                    end_date        varchar(255) NOT NULL,
                    end_time        varchar(255) NOT NULL,
                    project_name    varchar(255) NOT NULL,
                    definition      varchar(255) NOT NULL
                    )""").format(sql.Identifier(user)))
        
        # Asetetaan tietokantaan tallennettavat datat
        cur.execute(
            sql.SQL("""INSERT INTO {}(        
                start_date, 
                start_time, 
                end_date, 
                end_time, 
                project_name, 
                definition)
                VALUES (%s, %s, %s, %s, %s, %s)
                """).format(sql.Identifier(user)),(
                    tuntikirja.start_date,
                    tuntikirja.start_time,
                    tuntikirja.end_date,
                    tuntikirja.end_time,
                    tuntikirja.project_name,
                    tuntikirja.definition))

        # Suoritetaan datan tallennus tietokantaan
        conn.commit()

    except Exception as e:
        print(f"Tapahtui virhe, {e}")

    finally:
        if conn is not None:
            conn.close()


def check_if_table_exists(conn, cur):
    cur.execute("SELECT * FROM information_schema.tables WHERE table_name=%s", (user,))
    return bool(cur.rowcount)


if __name__ == "__main__":
    menu()



