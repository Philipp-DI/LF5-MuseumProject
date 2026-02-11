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
    
    STATUS_OPTIONS = ["Im Lager", "Ausgestellt", "Ungewiss"]
    
    id_counter = 1
    def __init__(self, title, creator, year, description, status, _uid=None, _id=None, **kwargs):
        self._uid = _uid if _uid else str(uuid.uuid4())
        if _id is not None:
            self._id = _id
            Exhibit.id_counter = max(Exhibit.id_counter, _id + 1)
        else:
            self._id = Exhibit.id_counter
            Exhibit.id_counter += 1
        
        self.title = title
        self.creator = creator
        self.year = year
        self.description = description
        self.status = status
        self.kh_epoche = self.determine_epoch()
        self.year_epoch_helper()
    
    def determine_epoch(self):
        if isinstance(self.year, int):
            for start, end, kh_epoche in Exhibit.EPOCHEN:
                if start <= self.year < end:
                    return kh_epoche
        return "Unbekannt"
    
    def year_epoch_helper(self):
        try:
            self.year = int(self.year)
        except ValueError:
            pass
        self.kh_epoche = self.determine_epoch()
    
    def update(self, title, creator, year, description, status, **kwargs):
        self.title = title
        self.creator = creator
        self.year = year
        self.description = description
        self.status = status
        self.year_epoch_helper()

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
        self.used_uids = set(ex._uid for ex in self.exhibits)

    def add_exhibit(self, exhibit):
        if exhibit._id in self.used_ids:
            raise ValueError(f"ID {exhibit._id} bereits vergeben.")
        if exhibit._uid in self.used_uids:
            raise ValueError(f"UID bereits vergeben.")
        self.used_ids.add(exhibit._id)
        self.used_uids.add(exhibit._uid)
        self.exhibits.append(exhibit)

    def list_exhibits(self):
        for exhibit in self.exhibits:
            print(exhibit.display_info())
            
    def get_exhibit_by_id(self, target_id):
        for ex in self.exhibits:
            if ex._id == target_id:
                return ex
        return None
        

# --- END of CLASSES ---

# --- FUNCTIONALITY ---
def run_inventory_app():
    museum = Museum()

    while True:
        print("\nCLI-based Museum Inventory App")
        print("[a] Exponat hinzufügen")
        print("[s] Exponat suchen")
        print("[l] Alle Exponate anzeigen oder editieren")
        print("[q] Speichern & Programm beenden")

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
        title = input("Titel: ")
        creator = input("Schöpfer/Künstler: ")
        year_raw = input("Jahr: ")
        description = input("Beschreibung: ")
        print("Status wählen:")
        for i, status in enumerate(Exhibit.STATUS_OPTIONS,1):
            print(f"[{i}]{status}\n")
        while True:
            try:
                choice = int(input())
                selected_status = Exhibit.STATUS_OPTIONS[choice - 1]
                break
            except (ValueError, IndexError):
                print("Ungültige Eingabe. Nummer aus Liste wählen.")
        status = selected_status

        # Optional: convert year to int
        try:
            year = int(year_raw)
        except ValueError:
            year = year_raw  # string is kept if conversion fails

        new_exhibit = Exhibit(title, creator, year, description, status)
        museum.add_exhibit(new_exhibit)
        print(f"Hinzugefügt:\n{new_exhibit.display_info()}")
        exit = input("Weiteres hinzufügen [a] oder zurück zum Menü: ").strip().lower()
        if exit != "a":
            return
        else:
            pass

def search_while_loop(museum):

    search_target = input("Suchbegriff eingeben: ").lower()
    index = 0
    found_exhibit = None 

    while index < len(museum.exhibits) and found_exhibit is None:
        current_exhibit = museum.exhibits[index]
        
        if (search_target in current_exhibit.title.lower() or
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

def edit_exhibit_flow(museum):
    try:
        target_id = int(input("Welche ID möchten Sie bearbeiten? "))
        exhibit = museum.get_exhibit_by_id(target_id)
        
        if exhibit:
            print(f"Bearbeite: {exhibit.title}")
            # Re-use the input logic to get new values
            new_title = input(f"Neuer Titel [{exhibit.title}]: ") or exhibit.title
            new_creator = input(f"Neuer Schöpfer [{exhibit.creator}]: ") or exhibit.creator
            new_year = input(f"Neues Jahr [{exhibit.year}]: ") or exhibit.year
            new_description = input(f"Neue Beschreibung [{exhibit.description}]: ") or exhibit.description
            new_status = input(f"Neuer Status [{exhibit.status}]: ") or exhibit.status
            # Call the renovation method we discussed
            exhibit.update(new_title, new_creator, new_year, new_description, new_status) 
            print("Änderungen gespeichert.")
        else:
            print("ID nicht gefunden.")
    except ValueError:
        print("Bitte eine gültige Nummer eingeben.")  
    
if __name__ == "__main__":
    run_inventory_app()