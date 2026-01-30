import statistics

def format_num(n):
    # Gibt Ganzzahl zurück, wenn möglich, sonst gerundeten Float.
    if isinstance(n, list):
        return [format_num(x) for x in n]
    return int(n) if n.is_integer() else round(n, 2)

def calculate_stats():
    data = []
    print("--- Statistik-Profi v5 ---")
    print("Eingabe: Zahlen (getrennt durch , ; oder Leerzeichen). 'calc' zum Rechnen.")

    while True:
        user_input = input("> ").strip().lower()
        if user_input == 'calc': break
        
        normalized = user_input.replace(',', ' ').replace(';', ' ')
        parts = normalized.split()
        
        for p in parts:
            try:
                data.append(float(p))
                print(f"✅ '{p}' hinzugefügt.")
                print(f"Aktueller Datensatz: {format_num(data)}")
            except ValueError:
                print(f"⚠️ '{p}' ignoriert.")

    if len(data) < 2:
        print("❌ Für Varianz/Standardabweichung werden mindestens 2 Werte benötigt!")
        return

    data.sort()
    
    # Berechnungen
    summe = sum(data)
    avg = sum(data) / len(data)
    med = statistics.median(data)
    modes = statistics.multimode(data)
    
    # Streuungsmaße
    spannweite = max(data) - min(data)
    varianz = statistics.variance(data)
    std_abw = statistics.stdev(data)

    print("\n" + "="*30)
    print(f"Daten (sortiert):   {format_num(data)} - in Summe: {format_num(summe)}")
    print("-" * 30)
    print(f"Durchschnitt:       {format_num(avg)}")
    print(f"Median:             {format_num(med)}")
    print(f"Modalwert(e):       {format_num(modes)}")
    print("-" * 30)
    print(f"Spannweite:         {format_num(spannweite)}")
    print(f"Varianz:            {format_num(varianz)}")
    print(f"Standardabw.:       {format_num(std_abw)}")
    print("="*30)

if __name__ == "__main__":
    calculate_stats()