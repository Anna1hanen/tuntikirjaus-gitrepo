from datetime import datetime
from datetime import time
from datetime import date

class Tuntikirja:
    def __init__(self):
        #self.date = aloituspäivä talteen loppupäivän vertailua varten
        self.end_date = end_date 
        self.end_time = end_time
        self.end_time_and_end_date = end_time_and_end_date
        self.start_date = start_date
        self.start_time = start_time
        self.start_time_and_start_date = start_time_and_start_date
        self.table = table
        
    def menu():
        return "Hello world!"

    def set_start_date():
        pass

    def set_start_time():
        pass

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

    def set_project():
        pass

    def input():
        pass
    
if __name__ == "__main__":
    #tunnit = Tuntikirja()
