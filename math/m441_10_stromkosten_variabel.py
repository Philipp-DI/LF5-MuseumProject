# Wie lassen sich die erwarteten Stromkosten eines Rechenzentrums bei variablen Lastzuständen digital modellieren?
import statistics as st
import matplotlib.pyplot as plot
import random as rd
# Grades & Weights
GRADES = [1, 2, 3]
WEIGHTS = [8 , 85, 7]

# Variable Lasten modellieren
def gen_last(grade):
    if grade == 1:
        return rd.randint(0, 100)
    elif grade == 2:
        return rd.randint(101, 500)
    elif grade == 3:
        return rd.randint(501, 1500)
    else: return 0

ZEITRAUM = {
    'Stunde': 1,
    'Tag': 24,
    'Monat': 24*30,
    'Jahr': 24*365
}
simulierte_last = []

for _ in range(ZEITRAUM['Monat']):
    weighted_choice = rd.choices(GRADES, weights=WEIGHTS, k=1)[0]
    simulierte_last.append(gen_last(weighted_choice))

# Extremwerte
minimale_last = min(simulierte_last)
maximale_last = max(simulierte_last)

# Mittelwert & Median
mittlere_last = sum(simulierte_last) / len(simulierte_last)
median_last = st.median(simulierte_last)

plot.plot(simulierte_last)
plot.xlabel('Stunde')
plot.ylabel('kW')
plot.title(f"Last/Stunde für den Zeitraum: {[k for k, v in ZEITRAUM.items() if v == len(simulierte_last)][0]}")
plot.show()
