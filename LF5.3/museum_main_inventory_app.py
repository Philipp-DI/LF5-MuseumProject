# 5.3: Museum Inventory App

import datetime as dt
import random as rd
import json as js
import uuid

# --- CLASSES ---
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
    def __init__(self, title, creator, year, description, status, uid=None, id=None, **kwargs):
        self._uid = uid or str(uuid.uuid4())
        if id is not None:
            self._id = id
            Exhibit.id_counter = max(Exhibit.id_counter, id + 1)
        else:
            self._id = Exhibit.id_counter
            Exhibit.id_counter += 1
        self.title = title
        self.creator = creator
        self.year = year
        self.description = description
        self.status = status
        self.kh_epoche = self.determine_epoch()
    
    def determine_epoch(self):
        try:
            self.year = int(self.year)
        except ValueError:
            self.year = self.year  # string is kept if conversion fails
        if isinstance(self.year, int):
            for start, end, kh_epoche in Exhibit.EPOCHEN:
                if start <= self.year < end:
                    return kh_epoche
        return "Unbekannt"

    def display_info(self):
        return f"ID: {self._id}\n Titel: {self.title}\n Schöpfer: {self.creator}\n Jahr/Epoche: {self.year}\n Beschreibung: {self.description}\n Status: {self.status}\n Kunsthistorische Epoche: {self.kh_epoche}\n"
    
class Museum:
    def __init__(self):
        try:
            with open("museum_exhibits.json", "r") as f:
                raw_data = js.load(f)
                # Hier passiert die Magie: Wir wandeln jedes Dict wieder in ein Objekt um
                self.exhibits = []
                for data in raw_data:
                    # Wir entpacken das Dictionary mit ** direkt in den Konstruktor
                    obj = Exhibit(**data)
                    self.exhibits.append(obj)
                
                print(f"{len(self.exhibits)} Exponate geladen.")
        except (FileNotFoundError, js.JSONDecodeError):
            print("Keine valide Exponatliste gefunden. Starte leer.")
            self.exhibits = []
        
        self.used_ids = set(ex._id for ex in self.exhibits)

    def add_exhibit(self, exhibit):
        if exhibit._id in self.used_ids:
            raise ValueError(f"ID {exhibit._id} ist bereits vergeben.")
        self.used_ids.add(exhibit._id)
        self.exhibits.append(exhibit)

    def list_exhibits(self):
        for exhibit in self.exhibits:
            print(exhibit.display_info())



# --- END of CLASSES ---

# --- FUNCTIONALITY ---
def run_inventory_app():
    museum = Museum()

    while True:
        print("\nCLI-based Museum Inventory App")
        print("[a] Exponat hinzufügen")
        print("[s] Exponat suchen")
        print("[l] Alle Exponate anzeigen")
        print("[q] Programm beenden")

        choice = input("Auswahl (a/s/l/q): ").strip().lower()

        if choice == "a":
            add_exhibits_flow(museum)
        elif choice == "s":
            search_while_loop(museum)
        elif choice == "l":
            museum.list_exhibits()
        elif choice == "q":
            # saving
            js.dump(
                [exhibit.__dict__ for exhibit in museum.exhibits],
                open("museum_exhibits.json", "w"),
                indent=4,
            )
            print("Programm wird beendet.")
            break
        else:
            print("Ungültige Eingabe. Bitte a, s, l oder q wählen.")

def add_exhibits_flow(museum: Museum):
    while True:
        action = input("\nNeues Exponat hinzufügen? (j/n): ").strip().lower()

        if action == 'j':
            name = input("Titel: ")
            creator = input("Schöpfer/Künstler: ")
            year_raw = input("Jahr: ")
            description = input("Beschreibung: ")
            status = input("Status (z.B. Ausgestellt, Im Lager): ")

            # Optional: convert year to int
            try:
                year = int(year_raw)
            except ValueError:
                year = year_raw  # string is kept if conversion fails

            new_exhibit = Exhibit(name, creator, year, description, status)
            museum.add_exhibit(new_exhibit)
            print(f"Hinzugefügt:\n{new_exhibit.display_info()}")
        elif action == 'n':
            break
        else:
            print("Bitte 'j' oder 'n' eingeben.")

def search_while_loop(museum):

    search_target = input("Suchbegriff eingeben: ").lower()
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
        print(f"\nSuche mit \"{search_target}\" ergab Treffer:\n{found_exhibit.display_info()}")
    else:
        print(f"\nDie Suche mit \"{search_target}\" ergab keine Treffer.")
        
if __name__ == "__main__":
    run_inventory_app()