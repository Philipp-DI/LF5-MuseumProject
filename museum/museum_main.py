# 5.3.4 - Imperative Programming

import datetime as dt
import random as rd
import json as js

class Exhibit:
    EPOCHEN = [
        (1945, 2026, "Zeitgenössische Kunst"),
        (1890, 1945, "Moderne"),
        (1848, 1890, "Realismus"),
        (1750, 1848, "Klassizismus / Romantik"),
        (1600, 1750, "Barock"),
        (1400, 1600, "Renaissance"),
        (500, 1400, "Mittelalter"),
        (-3000, 500, "Antike")
    ]
    
    id_counter = 1
    def __init__(self, title, creator, year, description, status):
        self.id = Exhibit.id_counter
        Exhibit.id_counter += 1
        self.name = title
        self.creator = creator
        self.year = year
        self.description = description
        self.status = status
        self.kh_epoche = self.determine_epoch()
    
    def determine_epoch(self):
        if isinstance(self.year, int):
            for start, end, kh_epoche in Exhibit.EPOCHEN:
                if start <= self.year < end:
                    return kh_epoche
        return "Unbekannt"

    def display_info(self):
        return f"ID: {self.id}\n Titel: {self.name}\n Schöpfer: {self.creator}\n Jahr/Epoche: {self.year}\n Beschreibung: {self.description}\n Status: {self.status}\n Kunsthistorische Epoche: {self.kh_epoche}\n"
    
class Museum:
    def __init__(self):
        self.exhibits = []
        self.used_ids = set()

    def add_exhibit(self, exhibit):
        if exhibit.id in self.used_ids:
            raise ValueError(f"ID {exhibit.id} ist bereits vergeben.")
        self.used_ids.add(exhibit.id)
        self.exhibits.append(exhibit)

    def list_exhibits(self):
        for exhibit in self.exhibits:
            print(exhibit.display_info())

    def find_exhibit_by_creator(self, creator_name):
        return [exhibit for exhibit in self.exhibits if exhibit.creator == creator_name]

def main():
    museum = Museum()

    exhibit1 = Exhibit("Spinnrad", "Unbekannt", "Biedermeier", "Ein altes Spinnrad, staubig, aber gut erhalten. Perfekt für Handwerksaustellung", "In Storage")
    exhibit2 = Exhibit("Römische Münze", "Unbekannt", "ca. 150 n. Chr.", "Eine römische Münze aus der Zeit des Kaisers Augustus.", "On Display")
    exhibit3 = Exhibit("Bürgermeister-Urkunde", "Stadt Oberdorfen", 1888, "Eine Urkunde des Bürgermeisters der Stadt Oberdorfen. ACHTUNG: Feuchtigkeitsschaden", "In Storage")

    museum.add_exhibit(exhibit1)
    museum.add_exhibit(exhibit2)
    museum.add_exhibit(exhibit3)

    print("Alle Stücke im Museum:")
    museum.list_exhibits()
    js.dump([exhibit.__dict__ for exhibit in museum.exhibits], open("museum_exhibits.json", "w"), indent=4)
    search_while_loop(museum)
    
def search_while_loop(museum):

    search_target = "peter".lower()
    index = 0
    found_exhibit = None 

    while index < len(museum.exhibits) and found_exhibit is None:
        current_exhibit = museum.exhibits[index]
        
        if (search_target in current_exhibit.name.lower() or
            search_target in current_exhibit.creator.lower() or
            search_target in str(current_exhibit.year).lower() or
            search_target in current_exhibit.description.lower() or
            search_target in current_exhibit.status.lower()):
            found_exhibit = current_exhibit
        else:
            index += 1

    if found_exhibit:
        print(f"Suche mit \"{search_target}\" ergab Treffer:\n{found_exhibit.display_info()}")
    else:
        print(f"Die Suche mit \"{search_target}\" ergab keine Treffer.")
        
if __name__ == "__main__":
    main()