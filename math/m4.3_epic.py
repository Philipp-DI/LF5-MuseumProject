# Import zusätzlicher Module 
import matplotlib.pyplot as plt
import math as m
import random as rd

# Blaupause für unsere Server / Antwortzeit-Struktur
class Server:
    alle_server = [] # Leere Liste anlegen in der wir alle Server ablegen
    # Der Konstruktor - hier "bauen" wir jedes Objekt
    def __init__(self, name: str, antwortzeiten: list[int]) -> None: # Diese Werte müssen "mitgeliefert" werden.
        self.name = name
        self.antwortzeiten = antwortzeiten
        # Diese Attribute werden erst innerhalb der Klasse zugewiesen/erstellt
        self.mittelwert = self.berechne_mittelwert()
        self.median = self.berechne_median()
        self.varianz = self.berechne_varianz()
        self.standardabweichung = self.berechne_standardabweichung()
        # Hier wird die Liste mit den konstruierten Objekten (Servern) gefüllt (jedes Objekt angehängt)
        Server.alle_server.append(self)
        
    @classmethod # Klassenmethode, damit wir außerhalb der Klasse auf die Funktion zugreifen können, ohne einzelne Objekte zuweisen zu müssen (betrachtet in unserem Fall dann alle konstruierten Objekte).
    def zeige_besten_server(cls):
        if cls.alle_server: # Wir führen die Funktion nur aus, wenn "alle_server" auch einen Wert hat und nicht leer ist.
            schnellster = min(cls.alle_server, key=lambda server: server.mittelwert) # Lambda ist eine "Platzhalter"- bzw. "Einwegfunktion"
            zuverlaessigster = min(cls.alle_server, key=lambda server: server.standardabweichung)
            
            print(f"\nBester Schnitt: {schnellster.name} ({schnellster.mittelwert:.2f}ms)")
            print(f"Konstantester:  {zuverlaessigster.name} (StdAbw: {zuverlaessigster.standardabweichung:.2f})")
        
    # Mittelwert berechnen ([Summe aller Werte] / [Gesamtzahl Iterationen])
    def berechne_mittelwert(self):
        # 1. Summe aller Elemente:
        # ALTERNATIV: summe = sum(self.antwortzeiten)
        summencontainer = 0 # Wir legen eine neue Variable, der wir Schritt für Schritt Werte addieren können.
        
        for x in self.antwortzeiten: # for-Schleife für jedes Element (x) wird Schritt für Schritt operiert, bis alle x-Elemente abgearbeitet sind.
            summencontainer += x # Hier wird in jedem Schritt das aktuelle x-Element aufaddiert.
            
        # 2. Summe durch Anzahl Elemente teilen:
        mittelwert = summencontainer / len(self.antwortzeiten) # Gesamtsumme wird dann durch die Anzahl der Elemente geteilt.
        return mittelwert

    # Median berechnen (Liste sortieren und den Wert in der Mitte finden)
    def berechne_median(self):
        sortierte_liste = sorted(self.antwortzeiten) # Liste wird in aufsteigende Reihenfolge sortiert und in eine neue Variable verpackt.
        if len(self.antwortzeiten) % 2 != 0: # Modulo Operator '%' prüft, ob es einen "Rest" gibt.
            mitte: int = int(len(self.antwortzeiten) / 2) # Wir identifizieren die Mitte (/-Operation rundet auf bei Umwandlung zu int).
            median = sortierte_liste[mitte]
            
        else: # Falls die Liste eine gerade Anzahl an Elementen hat, haben wir 2 Stellen in der Mitte.
            mitte: int = int(len(self.antwortzeiten) / 2)
            rechts = sortierte_liste[mitte] # Wir geben an "rechts" den Wert aus dem Index "mitte"
            links = sortierte_liste[mitte-1] # Wir geben an "links" den Wert um -1 verschoben.
            median = (rechts + links) / 2 # Mittelwert der 2 Stellen
        return median
    
    # Varianz berechnen
    def berechne_varianz(self):
        var = 0 # Varianz wird erstmal auf '0' gesetzt, damit wir keinen Unbound-Fehler bekommen
        for x in self.antwortzeiten:
            var += (x - self.mittelwert)**2 # Wir ziehen von jedem Element den Mittwelwert ab, quadrieren dann und addieren anschließend alles.
        varianz = ((var) / len(self.antwortzeiten)) # Populationsvarianz (Grundgesamtheit) / Stichprobenvarianz = (n - 1)
        return varianz
    
    # Standardabweichung berechnen
    def berechne_standardabweichung(self):
        stdabw = m.sqrt(self.varianz) # Standardabweichung ist die Quadratwurzel der Varianz (hier ist das "math"-Modul notwendig)
        return stdabw
    
    # Ausgabefunktion der Statistiken  
    def print_data(self):
        print(f"\n---| Statistik für {self.name} |---")
        
        # Formatierung: '20' Zeichen Platz frei halten, danach der Wert gerundet auf 2 Stellen
        print(f"{'Mittelwert:':20} {self.mittelwert:>8.2f} ms") # '>' = rechtsbündig, '8' = Breite für die Werte
        print(f"{'Median:':20} {self.median:>8.2f} ms")
        print(f"{'Varianz:':20} {self.varianz:>8.2f}")
        print(f"{'Standardbweichung:':20} {self.standardabweichung:>8.2f}")
        
    @classmethod
    def print_all_data(cls):
        if cls.alle_server: # Optionale Überprüfung, ob überhaupt Daten in "alle_server" sind. Nur dann wird ausgeführt
            for server in cls.alle_server:
                server.print_data()
    
    # Klassenmethode für das Erstellen der Diagramme
    @classmethod
    def plot_auswahl(cls, auswahl_liste: list): # Erwartet Übergabe einer Liste von Elementen
        plt.figure(figsize=(12, 8))
        if auswahl_liste == []: # Bedingung, wenn die Liste leer sein sollte
            for server in cls.alle_server:
                plt.plot(server.antwortzeiten, label=server.name, marker='o')
                # Annotation der Werte für alle Objekte leicht angepasst
                for i, value in enumerate(server.antwortzeiten):
                    plt.text(i, value +4, str(value), ha='center', fontsize=10)
            plt.title(f"Antwortzeiten für {len(cls.alle_server)} {cls.__name__}")
        else:
            for server in auswahl_liste: # Hier werden dann nur die Elemente aus der übergebenen Liste berücksichtigt
                plt.plot(server.antwortzeiten, label=server.name, marker='o')
                # Annotation der Werte innerhalb der anderen for-Schleife
                for i, value in enumerate(server.antwortzeiten):
                    plt.text(i, value +2, str(value), ha='center', fontsize=12)
            plt.title(f"Antwortzeiten für {len(auswahl_liste)} {cls.__name__}")

        # Feste Diagramm-Teile werden nur einmal außerhalb der Schleifen konstruiert
        plt.xlabel("Ping")
        plt.ylabel("Antwortzeit (ms)")
        plt.legend()
        plt.grid(True)
        plt.show()

# Hilfsfunktion zum Erstellen einer "zufälligen" Liste        
def zufalls_zeiten():
    zufallszeiten: list[int] = [rd.randint(10, 300) for _ in range(10)]
    return zufallszeiten

# Objekte nach Klassen-Blaupause "konstruieren/füttern":           
server_a = Server("Server A", [20, 85, 18, 92, 25, 15, 28, 88, 21, 23])
server_b = Server("Server B", [45, 42, 48, 40, 46, 41, 49, 43, 47, 44])
# Optionale bzw. zusätzliche Server zur Veranschaulichung
file_server = Server("File Server", zufalls_zeiten())
dns_server = Server("DNS Server", zufalls_zeiten())
cloud_server = Server("Cloud Server", zufalls_zeiten())


# Was hier drüber passiert ist IMMER da, auch wenn ich dieses Programm an anderer Stelle importiere/nutze.
if __name__ == "__main__": # Alles ab hier wird nur IN diesem Programm ausgeführt.
    Server.print_all_data()
    Server.zeige_besten_server()
    Server.plot_auswahl([]) # Bei leerer Liste (ohne Auswahl werden alle Server geplottet) 
    Server.plot_auswahl([server_b, server_a])