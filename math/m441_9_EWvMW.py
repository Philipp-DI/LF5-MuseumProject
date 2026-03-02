# Vergleich zwischen Erwartungswert und Mittelwert bei 1000 Zufallsereignissen.

import random

# Klassisches Würfelbeispiel (mal wieder)
ergebnisse = []
versuche = 1000
wuerfel = 100

# Ausführen
for x in range(versuche):
    ergebnisse.append(random.randint(1,wuerfel))
    
# Auswerten
wahrscheinlichkeit = 1 / wuerfel
moegliche_ergebnisse = list(range(1, wuerfel +1))

mittelwert = sum(ergebnisse) / versuche
erwartungswert = sum(e * wahrscheinlichkeit for e in moegliche_ergebnisse)

print(f"Verhätlnis zwischen MW und EW: {(mittelwert / erwartungswert):.3f}")
print("Je näher an [1] desto präziser das Experiment (-> Gesetz der Großen Zahlen)")