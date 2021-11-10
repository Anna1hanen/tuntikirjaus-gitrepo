
import psycopg2

from config import config

class Tuntikirja:
    def __init__(self, start_date = 0, end_date = 0, start_time = 0, end_time = 0, project_name = "", definition = ""):

        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.project_name = project_name
        self.definition = definition
        
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
    menu_commands = "1: Lisää uusi tuntikirja \n" \
                    "2: Katso kuluneen viikon tuntikirjaukset \n" \
                    "3: Poistu\n>"
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
                print(f"Virheellinen syöte, {e}")

    def make_new_worklog():
        tuntikirja = Tuntikirja()
        tuntikirja.set_project_name()
        tuntikirja.set_definition()
        tuntikirja.insert_to_database()


    
    menu()