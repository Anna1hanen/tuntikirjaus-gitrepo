import datetime
import json
from config import config
import psycopg2
import psycopg2.sql as sql
from Crypto.Hash import SHA256
import requests 


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
                date_entry = input("Anna aloituspäivämäärä muodossa DD/MM/YYYY\n> ")
                if len(date_entry) != 10:
                    print("Syöte on väärän mittainen, yritä uudelleen")
                    continue
                else:
                    day, month, year = map(int, date_entry.split('/'))
                    self.start_date = datetime.date(year, month, day)
                    return self.start_date
            except Exception as e:
                print(f"Virheellinen syöte, {e}")
                continue

    def set_start_time(self):
        while True:
            try:
                date_entry = input("Anna aloitusaika muodossa HH:MM\n> ")
                if len(date_entry) != 5:
                    print("Syöte on väärän mittainen, yritä uudelleen")
                    continue
                else:
                    hour, minute = map(int, date_entry.split(':'))
                    self.start_time = datetime.time(hour, minute)
                    self.start_time = self.start_time.strftime("%H:%M")
                    return self.start_time
            except Exception as e:
               print(f"Virheellinen syöte, {e}")

    def set_end_date(self):
        while True:
            try:
                enddate_entry = input("Anna lopetuspäivä muodossa DD/MM/YYYY\n> ")
                if len(enddate_entry) != 10:
                    print("Syöte on väärän mittainen, yritä uudelleen")
                    continue
                else:
                    day, month, year = map(int, enddate_entry.split('/'))
                    self.end_date = datetime.date(year, month, day)
                    while True:
                        if self.start_date > self.end_date:
                            while True:
                                try:
                                    valinta = int(input(
                                        f"Lopetuspäivämäärä ({self.end_date}) on ennen aloituspäivämäärää ({self.start_date})\n1: Vaihda aloituspäivä\n2: Vaihda lopetuspäivä\n> "))
                                    if valinta == 1:
                                        self.set_start_date()

                                        break
                                    elif valinta == 2:
                                        self.set_end_date()
                                        break
                                    else:
                                        print("Virheellinen komento, yritä uudelleen")
                                        continue
                                except Exception as e:
                                    print(f"Virheellinen syöte, {e}")
                                    continue

                        else:
                            return self.end_date
                    

            except Exception as e:
                print(f"Virheellinen syöte, {e}")
                continue

             
    def set_end_time(self):
        while True:
            try:
                endtime_entry = input("Anna lopetusaika muodossa HH:MM\n> ")
                if len(endtime_entry) != 5:
                    print("Syöte on väärän mittainen, yritä uudelleen")
                    continue
                else:
                    hour, minute = map(int, endtime_entry.split(':'))
                    self.end_time = datetime.time(hour, minute)
                    self.end_time = self.end_time.strftime("%H:%M")

                    while True:

                        if self.start_date > self.end_date:
                            valinta = int(input(f"Työn lopetusajankohta ({self.end_time}) ei voi olla ennen aloitusajankohtaa ({self.start_time}).\n1: Vaihda aloitusajankohta\n2: Vaihda lopetusajankohta\n> "))
                            if valinta == 1:
                                self.set_start_date()
                            elif valinta == 2:
                                self.set_end_date()
                            else:
                                print("Virheellinen syöte, yritä uudelleen")

                        elif self.start_date < self.end_date:
                            return self.end_time

                        elif self.start_date == self.end_date:
                            if self.end_time <= self.start_time:
                                valinta = int(input(f"Antamasi lopetuskellonaika ({self.end_time}) on joko sama tai ennen aloituskellonaikaa ({self.start_time}).\n1: Vaihda aloituspäivä\n2: Vaihda aloitusaika\n3: Vaihda lopetuspäivä \n4: Vaihda lopetusaika\n> "))
                                if valinta == 1:
                                    self.set_start_date()
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
                continue
  
    def set_project_name(self):
        while True:
            try:
                project_name_entry = input("Anna projektin nimi: \n> ")
                if len(project_name_entry) < 1 or len(project_name_entry) > 50:
                    print("Syöte on väärän mittainen, syötteen tulee olla väliltä 1 ja 50, yritä uudelleen")
                    continue
                else:
                    self.project_name = project_name_entry
                    return self.project_name
            except Exception as e:
                print(f"Virheellinen syöte, {e}")
                continue

    
    def set_definition(self):
        while True:
            try:
                definition_entry = input("Anna työskentelyn sisältö: \n> ")
                if len(definition_entry) < 1 or len(definition_entry) > 255:
                    print("Syöte on väärän mittainen, syötteen tulee olla väliltä 1 ja 255, yritä uudelleen")
                    continue
                else:
                    self.definition = definition_entry
                    return self.definition
            except Exception as e:
                print(f"Virhe tapahtui, {e}")
                continue


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
                    "3: Kirjaudu ulos\n> "

    while True:
        try:
            print(f"\nKirjautuneena sisään käyttäjällä: {user}\n")
            command = int(input(menu_commands))
            if command == 1:
                # tee uusi tuntikirja
                make_new_worklog(user)
            elif command == 2:
                select_from_table(user)
                pass
            elif command == 3:
                # kirjautuu ulos
                user = None
                login_window()
            else:
                print("Virheellinen syöte")
        except Exception as e:
            # tuli virhe jossain päin koodia

            #raise tarkempaa testausta varten
            # raise e

            # raaka errorin printti
            print(f"Virheellinen syöte, {e}")

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
    conn = None
    try:
        # Laitetaan data databaseen
        conn = psycopg2.connect(**config())
        cur = conn.cursor()
        if check_if_table_exists(cur, user):
            # table for the user already exists
            pass
        # jos ei; luodaan uusi taulu
        else:
            cur.execute(
                sql.SQL("""CREATE TABLE {}(
                    id              serial primary key,
                    start_date      varchar(11) NOT NULL,
                    start_time      varchar(6) NOT NULL,
                    end_date        varchar(11) NOT NULL,
                    end_time        varchar(6) NOT NULL,
                    project_name    varchar(51) NOT NULL,
                    definition      varchar(255) NOT NULL,
                    weather         varchar(255) NOT NULL
                    )""").format(sql.Identifier(user)))

        # Haetaan säädata
        temp, samu = get_weather_data()

        weather = f"Lämpötila Phuketissa on {str(temp)} C, {samu}"
        # Asetetaan tietokantaan tallennettavat datat
        cur.execute(
            sql.SQL("""INSERT INTO {}(        
                start_date, 
                start_time, 
                end_date, 
                end_time, 
                project_name, 
                definition,
                weather)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """).format(sql.Identifier(user)),(
                    tuntikirja.start_date,
                    tuntikirja.start_time,
                    tuntikirja.end_date,
                    tuntikirja.end_time,
                    tuntikirja.project_name,
                    tuntikirja.definition,
                    weather))

        # Suoritetaan datan tallennus tietokantaan
        conn.commit()

    except Exception as e:
        print(f"Tapahtui virhe 1, {e}")
        #raise e
    finally:
        if conn is not None:
            conn.close()


def select_from_table(user):
    conn = None
    try:
        # Hae viimeisimmät kirjaukset
        conn = psycopg2.connect(**config())
        cur = conn.cursor()
        cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(user)))
        rows = cur.fetchall()

        if rows is not None:
            print(f"{user}")
            for row in rows:
                print(f"{row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]} - {row[6]} - {row[7]}")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        # raise error

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
            print(f"Tapahtui virhe 2, {e}")
            # raise e


def register():
    conn = None
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
                            username varchar(21) NOT NULL,
                            password varchar(255) NOT NULL
                        )
                    """)
        while True:
            command = int(input("1: Rekisteröidy\n"
                                "2: Poistu\n> "))
            if command == 2:
                break
            elif command == 1:
                username = input("Anna käyttäjänimi\n> ")
                if len(username) < 1 or len(username) > 20:
                    print("Syöte on väärän mittainen, syötteen tulee olla väliltä 1 ja 20, yritä uudelleen")
                    continue
                else:
                    password = input("Anna salasana\n> ")
                    if len(password) < 1 or len(password) > 30:
                        print("Syöte on väärän mittainen, syötteen tulee olla väliltä 1 ja 30, yritä uudelleen")
                        continue
                    else:
                        password2 = input("Anna salasana uudelleen\n> ")
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
        #raise e
        print(f"Tapahtui virhe 3, {e}")

    finally:
        if conn is not None:
            conn.close()


def login():
    conn = None
    try:
        conn = psycopg2.connect(**config())
        cur = conn.cursor()
        while True:
            command = int(input("1: Kirjaudu\n"
                                "2: Poistu\n> "))
            if command == 2:
               break

            elif command == 1:

                username = input("Anna käyttäjänimi\n> ")
                password = input("Anna salasana\n> ")
                encoded_password = str.encode(password)
                hashed_password = SHA256.new()
                hashed_password.update(encoded_password)
                binary_password_string = hashed_password.digest()

                cur.execute("SELECT username FROM users WHERE username=%s AND password=%s", (username,str(binary_password_string)))

                if bool(cur.rowcount) is True:
                    returned_user = cur.fetchone()[0]
                    user = returned_user
                    menu(user)
                else:
                    print("Väärä käyttäjänimi tai salasana")
            else:
                print("Virheellinen komento")

    except Exception as e:
        print(f"Tapahtui virhe 4, {e}")
        # raise e
    finally:
        if conn is not None:
            conn.close()


def get_weather_data():
    api_key = "340ff6fa90f384a37b7784ac9a150849"
    city_id = "1151254"
    api_call = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}"
    response = requests.get(api_call)
    data = json.loads(response.text)

    for key, value in data.items():
        if key == "main":
            kelvin = value["temp"]
            celsius = kelvin - 273.15
            temp = ("%.1f" % celsius)
            samu = ""
            if celsius > 50:
                samu = "Samu on tulessa"
            elif celsius > 40:
                samu = "Samulla on helevetin kuuma"
            elif celsius > 30:
                samu = "Samulla on kuuma"
            elif celsius > 25:
                samu = "Samulla on aika lämmin"
            elif celsius > 20:
                samu = "Samulla on sopiva"
            elif celsius > 15:
                samu = "Samun mielestä sais olla vähän lämpimämpi"
            elif celsius > 10:
                samu = "Samulla on viileä"
            elif celsius > 5:
                samu = "Samulla on kylmä"
            elif celsius > 0:
                samu = "Samua palelee"
            elif celsius < -50:
                samu = "Samu on jäätynyt"
            else:
                samu = "Thaimaa on jäässä mutta Samu sinnittelee vielä samalla kun thaimaalaiset jäätyvät ympärillä"
            return temp, samu


if __name__ == "__main__":
    login_window()



