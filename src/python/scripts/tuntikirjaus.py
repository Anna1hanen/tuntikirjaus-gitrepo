import datetime
from config import config
import psycopg2
import psycopg2.sql as sql
from Crypto.Hash import SHA256

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

        try:
            enddate_entry = input("Anna lopetuspäivä muodossa DD/MM/YYYY\n>")
            day, month, year = map(int, enddate_entry.split('/'))
            self.end_date = datetime.date(year, month, day)

            if self.start_date > self.end_date:
                valinta = int(input(f"Lopetuspäivämäärä ({self.end_date}) on ennen aloituspäivämäärää ({self.start_date}), haluaisitko muuttaa aloituspäivän? Valitse 1, jos haluat muuttaa aloituspäivän. Valitse 2, jos haluat muuttaa lopetuspäivän. \n"))
                if valinta == 1:
                    self.set_start_date()
                elif valinta ==2:
                    self.set_end_date()
        except Exception as e:
            print(f"Virheellinen syöte, {e}")
             
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
        self.project_name = input("Anna projektin nimi: ")
        return self.project_name

    
    def set_definition(self):
        self.definition = input("Anna työskentelyn sisältö: ")
        return self.definition


    def __str__(self):
        return f"Aloitus päivä: {self.start_date}\n" \
               f"Aloitus aika: {self.start_time}\n" \
               f"Lopetus päivä: {self.end_date}\n" \
               f"Lopetus aika: {self.end_time}\n" \
               f"Projektin nimi: {self.project_name}\n" \
               f"Selite: {self.definition}"


def menu(user):
    menu_commands = "1: Lisää uusi tuntikirja \n" \
                    "2: Katso kuluneen viikon tuntikirjaukset \n" \
                    "3: Kirjaudu ulos\n>"

    while True:
        try:
            print(f"Kirjautuneena sisään käyttäjällä: {user}")
            command = int(input(menu_commands))
            if command == 1:
                # tee uusi tuntikirja
                make_new_worklog(user)
            elif command == 2:
                # katso tuntikirjaukset
                pass
            elif command == 3:
                # kirjautuu ulos
                user = None
                login_window()
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


def make_new_worklog(user):
    tuntikirja = Tuntikirja()
    tuntikirja.set_start_date()
    tuntikirja.set_start_time()
    tuntikirja.set_end_date()
    tuntikirja.set_end_time()
    tuntikirja.set_project_name()
    tuntikirja.set_definition()
    print("Uusi tuntikirjaus lisätty")
    print(f"\n{tuntikirja}\n")

    insert_to_database(tuntikirja, user)


def insert_to_database(tuntikirja, user):
    con = None
    try:
        # Laitetaan data databaseen
        conn = psycopg2.connect(**config())
        cur = conn.cursor()
        if check_if_table_exists(cur, user):
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
                """).format(sql.Identifier(user)), (
                tuntikirja.start_date,
                tuntikirja.start_time,
                tuntikirja.end_date,
                tuntikirja.end_time,
                tuntikirja.project_name,
                tuntikirja.definition,)
        )
        conn.commit()

    except Exception as e:
        # print(f"Tapahtui virhe 1, {e}")
        raise e
    finally:
        if conn is not None:
            conn.close()


def check_if_table_exists(cur, table):
    cur.execute("SELECT * FROM information_schema.tables WHERE table_name=%s", (table,))
    return bool(cur.rowcount)

def check_if_user_exists(cur, username):
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    return bool(cur.rowcount)

def login_window():
    login_window_commands = "1: Kirjaudu sisään \n" \
                            "2: Rekisteröidy \n" \
                            "3: Poistu\n>"

    while True:
        try:
            print("Et ole kirjautuneena sisään\n")
            command = int(input(login_window_commands))
            if command == 1:
                # kirjaudu sisään
                login()
            elif command == 2:
                # rekisteröidy
                register()
            elif command == 3:
                # lopettaa ohjelman
                quit()
            else:
                print("Virheellinen syöte")
        except Exception as e:
            # print(f"Tapahtui virhe 2, {e}")
            raise e


def register():
    con = None
    try:
        # Laitetaan data databaseen
        conn = psycopg2.connect(**config())
        cur = conn.cursor()
        if check_if_table_exists(cur, "users"):
            # table for the user already exists
            pass
        else:
            # tehdään table kayttajat
            cur.execute(
                    """
                        CREATE TABLE users (
                            id serial primary key,
                            username varchar(255) NOT NULL,
                            password varchar(255) NOT NULL
                        )
                    """)
        while True:
            command = int(input("1: Rekisteröidy\n"
                                "2: Poistu\n>"))
            if command == 2:
                break
            elif command == 1:
                username = input("Anna käyttäjänimi\n>")
                password = input("Anna salasana\n>")
                password2 = input("Anna salasana uudelleen\n>")
                if password == password2:
                    # Tarkistetaan onko käyttäjänimi jo olemassa
                    if check_if_user_exists(cur, username):
                        # Käyttäjänimi on jo olemassa
                        print("Käyttäjänimi on varattu")
                        pass
                    else:
                        encoded_password = str.encode(password)
                        hashed_password = SHA256.new()
                        hashed_password.update(encoded_password)
                        binary_password_string = hashed_password.digest()
                        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, str(binary_password_string),))

                        conn.commit()
                        break
                else:
                    print("Salasanat eivät täsmää")
            else:
                print("Virheellinen komento, yritä uudelleen")

    except Exception as e:
        raise e
        # print(f"Tapahtui virhe 3, {e}")

    finally:
        if conn is not None:
            conn.close()


def login():
    con = None
    try:
        conn = psycopg2.connect(**config())
        cur = conn.cursor()
        while True:
            command = int(input("1: Kirjaudu\n"
                                "2: Poistu\n>"))
            if command == 2:
                break

            elif command == 1:
                username = input("Anna käyttäjänimi\n>")
                password = input("Anna salasana\n>")
                encoded_password = str.encode(password)
                hashed_password = SHA256.new()
                hashed_password.update(encoded_password)
                binary_password_string = hashed_password.digest()


                cur.execute("SELECT username FROM users WHERE username=%s AND password=%s", (username, str(binary_password_string),))
                if bool(cur.rowcount) is True:
                    returned_user = cur.fetchone()[0]
                    user = returned_user
                    menu(user)
                else:
                    print("Väärä käyttäjänimi tai salasana")
            else:
                print("Virheellinen komento")

    except Exception as e:
        #print(f"Tapahtui virhe 4, {e}")
        raise e
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    login_window()



