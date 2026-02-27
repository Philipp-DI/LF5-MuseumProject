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
        self.exhibits = []
        self.galleries = []
        try:
            with open("museum_exhibits.json", "r") as f:
                data = js.load(f)
                # If old format (list), handle gracefully
                if isinstance(data, list):
                    self.exhibits = [Exhibit(**d) for d in data]
                else:
                    # New format (dict)
                    self.exhibits = [Exhibit(**d) for d in data.get("exhibits", [])]
                    for g_data in data.get("galleries", []):
                        gal = Gallery(g_data["name"], g_data["start"], g_data["end"], g_data["location"])
                        gal.exhibit_ids = g_data["exhibit_ids"]
                        self.galleries.append(gal)
                print(f"{len(self.exhibits)} Exponate und {len(self.galleries)} Galerien geladen.")
        except (FileNotFoundError, js.JSONDecodeError):
            print("Nichts gefunden. Starte leer.")
        
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
        choice = input("Zum Starten der Bearbeitung [b] eingeben: ")
        if choice == "b":
            update_exhibit_flow(self)
        else:
            pass
            
    def get_exhibit_by_id(self, target_id):
        for ex in self.exhibits:
            if ex._id == target_id:
                return ex
        return None

class Gallery:
    def __init__(self, name, start, end, location) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.location = location
        self.exhibit_ids = []
        
    def add_ex_to_gallery(self, museum, target_id):
        exhibit = museum.get_exhibit_by_id(target_id)
        if not exhibit:
            print("ID nicht gefunden.")
            return
        
        if exhibit.status == "Ausgestellt":
            confirm = input(f"Objekt bereits ausgestellt! Trotzdem hinzufügen [j]?: ").strip().lower()
            if confirm != "j":
                return
        
        if target_id not in self.exhibit_ids:
            self.exhibit_ids.append(target_id)
            print(f"{exhibit.title} mit der ID: {exhibit._id} wurde der Galerie '{self.name}' hinzugefügt.")
        else:
            print(f"{exhibit.title} ist bereits Teil dieser Galerie.")
    
    def remove_ex_from_gallery(self, museum, target_id):
        exhibit = museum.get_exhibit_by_id(target_id)
        if target_id in self.exhibit_ids:
            confirm = input(f"Exponat {target_id} wirklich aus '{self.name}' entfernen? [j/n]: ").strip().lower()
            if confirm != "j":
                print("Vorgang abgebrochen.")
                return
            self.exhibit_ids.remove(target_id)
        else:
            print("ID nicht in Galerie gefunden!")
            return
        if exhibit:
            print(f"'{exhibit.title}' wurde aus der Galerie entfernt.")
    
    def display_gallery(self, museum):
        print(f"---- {self.name} ----")
        if not self.exhibit_ids:
            print("Zurzeit keine Objekte hier.")
            return
        
        for target_id in self.exhibit_ids:
            exhibit = museum.get_exhibit_by_id(target_id)
            if exhibit:
                print(f"ID: {exhibit._id} --- {exhibit.title}")
            else:
                print("ID nicht gefunden.")

# --- END of CLASSES ---

# --- FUNCTIONALITY ---
def run_inventory_app():
    museum = Museum()

    while True:
        print("\n🧭>> CLI-based Museum Inventory App <<🧭")
        print("[1] Exponat hinzufügen")
        print("[2] Exponat suchen")
        print("[3] Alle Exponate anzeigen und/oder editieren")
        print("[4] Galerie erstellen oder bearbeiten")
        print("[Q] Speichern & Programm beenden")

        choice = input("Auswahl: ").strip().lower()

        if choice == "1":
            add_exhibits_flow(museum)
        elif choice == "2":
            search_while_loop(museum)
        elif choice == "3":
            museum.list_exhibits()
        elif choice == "4":
            gallery_flow(museum)
        elif choice == "q":
            # The "Envelope" structure
            full_inventory = {
                "exhibits": [ex.__dict__ for ex in museum.exhibits],
                "galleries": [
                    {
                        "name": gal.name, 
                        "start": gal.start, 
                        "end": gal.end, 
                        "location": gal.location, 
                        "exhibit_ids": gal.exhibit_ids
                    } for gal in museum.galleries
                ]
            }
            with open("museum_exhibits.json", "w") as f:
                js.dump(full_inventory, f, indent=4)
            print("Daten gespeichert. Programm beendet!")
            break
        else:
            print("Ungültige Eingabe.")

def status_selector(current_status=None):
    suffix = f" [Aktueller Status: {current_status}]" if current_status else ""
    print(f"Status wählen{suffix}:")
    for i, status in enumerate(Exhibit.STATUS_OPTIONS,1):
        print(f"[{i}]{status}\n")
    while True:
        user_input = input("Wählen oder Enter zum Beibehalten: ").strip()
        if current_status and not user_input:
            return current_status
        try:
            choice = int(user_input)
            return Exhibit.STATUS_OPTIONS[choice - 1]
        except (ValueError, IndexError):
            print("Ungültige Eingabe. Nummer aus Liste wählen.")

def add_exhibits_flow(museum: Museum):
    while True:
        title = input("Titel: ")
        creator = input("Schöpfer/Künstler: ")
        year = input("Jahr: ")
        description = input("Beschreibung: ")
        status = status_selector()

        new_exhibit = Exhibit(title, creator, year, description, status)
        museum.add_exhibit(new_exhibit)
        print(f"Hinzugefügt:\n{new_exhibit.display_info()}")
        exit = input("Weiteres hinzufügen [a] oder zurück zum Menü: ").strip().lower()
        if exit != "a":
            return
        else:
            pass

def search_while_loop(museum: Museum):
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

def update_exhibit_flow(museum: Museum):
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
            new_status = status_selector(exhibit.status)
            # Call the renovation method we discussed
            exhibit.update(new_title, new_creator, new_year, new_description, new_status)
            print("Änderungen gespeichert.")
        else:
            print("ID nicht gefunden.")
    except ValueError:
        print("Bitte eine gültige Nummer eingeben.")  
    
def create_gallery(museum: Museum):
    while True:
        name = input("Name der Galerie: ")
        if not name:
            print("Name darf nicht leer sein!")
            return
        start = input("Startdatum: ")
        end = input("Enddatum: ")
        location = input("Ort: ")
        
        new_gallery = Gallery(name, start, end, location)
        museum.galleries.append(new_gallery)
        print("Galerie wurde erfolgreich angelegt")
        exit = input("Weitere hinzufügen [1] oder zurück zum Menü: ").strip().lower()
        if exit != "1":
            return
        else:
            pass

def show_galleries(museum: Museum):
    if not museum.galleries:
        print("Es existieren noch keine Galerien.")
        return
    print("\nVerfügbare Galerien:")
    for i, gal in enumerate(museum.galleries, 1):
        print(f"[{i}] {gal.name}")
    try:
        idx = int(input("Welche Galerie anzeigen? (Nummer): ")) - 1
        if idx <= 0 or idx >= len(museum.galleries):
            print("Ungültige Auswahl.")
            return
        selected_gallery = museum.galleries[idx]
        selected_gallery.display_gallery(museum)
    except (ValueError, IndexError):
        print("Ungültige Auswahl.")
        return
        
def add_to_gallery(museum: Museum):
    if not museum.galleries:
        print("Es existieren noch keine Galerien.")
        new = input("Jetzt eine neue Galerie erstellen? [j]")
        if new != "j":
            return
        else:
            create_gallery(museum)
            
    print("\nVerfügbare Galerien:")
    for i, gal in enumerate(museum.galleries, 1):
        print(f"[{i}] {gal.name}")
    try:
        idx = int(input("Welche Galerie bearbeiten? (Nummer): ")) - 1
        if idx <= 0 or idx >= len(museum.galleries):
            print("Ungültige Auswahl.")
            return
        selected_gallery = museum.galleries[idx]
        add_or_del = input(f"[1] Objekte der Galerie '{selected_gallery.name}' hinzufügen\n[2] Objekte aus '{selected_gallery.name}' entfernen\n").strip().lower()
        if add_or_del == "1":
            if not museum.exhibits:
                print("Es gibt noch keine Exponate im Museum. Bitte zuerst Exponate anlegen.")
                return
            print(f"Liste der Exponate:\n")
            for exhibit in museum.exhibits:
                print(exhibit.display_info())
            try:
                target_id = int(input("Welche Exponat-ID möchten Sie hinzufügen? "))
            except ValueError:
                print("Ungültige Eingabe.")
                return
            selected_gallery.add_ex_to_gallery(museum, target_id)
        elif add_or_del == "2":
            print(f"In '{selected_gallery.name}' befinden sich:\n")
            selected_gallery.display_gallery(museum)
            try:
                target_id = int(input("Welche Exponat-ID möchten Sie entfernen? "))
            except ValueError:
                print("Ungültige Eingabe.")
                return
            selected_gallery.remove_ex_from_gallery(museum, target_id)
        else:
            print("Ungültige Auswahl.")
            return
    except (ValueError, IndexError):
        print("Ungültige Auswahl.")
        
def gallery_flow(museum: Museum):
    while True:
        print("\n>> 🖼️ Galerie-Verwaltung 🖼️ <<")
        print("[1] Neue Galerie erstellen")
        print("[2] Galerie-Inhalt anzeigen")
        print("[3] Exponat einer Galerie hinzufügen oder entfernen")
        print("[H] Zurück zum Hauptmenü")
        
        choice = input("Auswahl: ").strip().lower()
        if choice == "1":
            create_gallery(museum)
        elif choice == "2":
            show_galleries(museum)
        elif choice == "3":
            add_to_gallery(museum)
        elif choice == "h":
            break
        else:
            print("Ungültige Auswahl.")
            return

if __name__ == "__main__":
    run_inventory_app()