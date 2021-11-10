import datetime
from src.python.data.config import config as config
import psycopg2
import psycopg2.sql as sql

menu_commands = "1: Lisää uusi tuntikirja \n" \
                "2: Katso kuluneen viikon tuntikirjaukset \n" \
                "3: Poistu\n>"

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
        end_time_and_end_date = datetime.date.self.end_date + datetime.time.self.end_time
        start_time_and_start_date = datetime.date.self.start_date + datetime.time.self.end_time
        if start_time_and_start_date > end_time_and_end_date:
            valinta = input(f"Työn lopetusajankohta ({self.end_time}) ei voi ennen aloitusajankohtaa ({self.start_time}). Haluatko muuttaa aloitusajankohtaa? Vastaa k, jos haluat")
            if valinta == 'k' or valinta == 'K':
                return self.set_start_date()
        
            return self.end_time

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

    def set_definition(self):

        pass

    def __str__(self):
        return f"Aloitus päivä: {self.start_date}\n" \
               f"Aloitus aika: {self.start_time}\n" \
               f"Lopetus päivä: {self.end_date}\n" \
               f"Lopetus aika: {self.end_time}\n" \
               f"Projektin nimi: {self.project_name}\n" \
               f"Selite: {self.definition}"


def menu():
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
    print(tuntikirja)

    insert_to_database(tuntikirja)


def insert_to_database(tuntikirja):
    # Laitetaan data databaseen
    conn = psycopg2.connect(**config())
    cur = conn.cursor()
    if check_if_table_exists(conn, cur):
        # table for the user already exists
        pass
    else:
        # Create new table with username
        cur.execute(
            sql.SQL("""
        CREATE TABLE {} (
            id serial primary key,
            start_date varchar(255) NOT NULL,
            start_time varchar(255) NOT NULL,
            end_date varchar(255) NOT NULL,
            end_time varchar(255) NOT NULL,
            project_name varchar (255) NOT NULL,
            definition varchar(255) NOT NULL
        )
        """).format(sql.Identifier(user)))


    cur.execute(
        sql.SQL("""
    INSERT INTO {} (start_date, start_time, end_date, end_time, project_name, definition)
    VALUES (%s, %s, %s, %s, %s, %s)
    """).format(sql.Identifier(user)), (tuntikirja.start_date, tuntikirja.start_time, tuntikirja.end_date, tuntikirja.end_time, tuntikirja.project_name, tuntikirja.definition,))
    conn.commit()


def check_if_table_exists(conn, cur):
    cur.execute("SELECT * FROM information_schema.tables WHERE table_name=%s", (user,))
    return bool(cur.rowcount)


if __name__ == "__main__":
    menu()


