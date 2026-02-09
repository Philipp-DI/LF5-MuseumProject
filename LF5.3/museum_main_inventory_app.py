# 5.3: Museum Inventory App

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
            try:
                with open("museum_exhibits.json", "r") as f:
                    raw_data = js.load(f)
                    # Hier passiert die Magie: Wir wandeln jedes Dict wieder in ein Objekt um
                    self.exhibits = []
                    for data in raw_data:
                        # Wir entpacken das Dictionary mit ** direkt in den Konstruktor
                        obj = Exhibit(data['name'], data['creator'], data['year'], 
                                    data['description'], data['status'])
                        self.exhibits.append(obj)
                    
                    print(f"Lade {len(self.exhibits)} Exponate als Objekte.")
            except (FileNotFoundError, js.JSONDecodeError):
                print("Keine valide Exponatliste gefunden. Starte leer.")
                self.exhibits = []
            
            self.used_ids = set(ex.id for ex in self.exhibits)

    def add_exhibit(self, exhibit):
        if exhibit.id in self.used_ids:
            raise ValueError(f"ID {exhibit.id} ist bereits vergeben.")
        self.used_ids.add(exhibit.id)
        self.exhibits.append(exhibit)

    def list_exhibits(self):
        for exhibit in self.exhibits:
            print(exhibit.display_info())

def run_inventory_app():
    museum = Museum()
    print("CLI-based Museum Inventory App\n")
    print("Möchten Sie Exponate hinzufügen [a], suchen [s] oder die Liste anzeigen [l]?")
    choice = input("Warte auf Eingabe... (a/s/l)").lower()
    if choice == "s":
        search_while_loop(museum)
        return
    elif choice == "l":
        museum.list_exhibits()
        return
    elif choice == "a":
        pass
    else:
        print("Ungültige Eingabe. Beende Programm.")
        return
    
    running = True
    while running:
        action = input("\nNeues Exponat hinzufügen? (j/n): ").lower()
        
        if action == 'j':
            name = input("Titel: ")
            creator = input("Schöpfer/Künstler: ")
            year = input("Jahr: ")
            description = input("Beschreibung: ")
            status = input("Status (z.B. Ausgestellt, Im Lager): ")
            
            new_exhibit = Exhibit(name, creator, year, description, status)
            museum.add_exhibit(new_exhibit)
            print(f"Hinzugefügt: {new_exhibit}")
        
        elif action != 'j':
            running = False
    
    print("\nListe der Exponate im Museum:")
    museum.list_exhibits()
    print(f"\nGesamtanzahl: {len(museum.exhibits)} Exponate.")

    js.dump([exhibit.__dict__ for exhibit in museum.exhibits], open("museum_exhibits.json", "w"), indent=4)

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
    run_inventory_app()