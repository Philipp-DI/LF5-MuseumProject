import matplotlib.pyplot as plot

CHANCES = { 'probs': {
    'Blau': 0.870,
    'Violett': 0.128,
    'Gold': 0.04 }
    } # Gesamt Wahrscheinlichkeit "egal", wird normalisiert

# Werte normalisieren (Gesamtwahrscheinlichkeit auf 1 bringen, kann u.U. 0,9999999... ergeben)
def normalisieren(data):
    gesamt_p = sum(CHANCES['probs'].values())
    return {k: p / gesamt_p for k, p in data.items()}

normiert = normalisieren(CHANCES['probs'])
pruef = sum(normiert.values())

# Optionale Bedingung: Diagramm wird nur erstellt, wenn Gesamt P = 1
if sum(normiert.values()) == 1:
    # Daten parsen
    x_keys = list(normiert.keys())
    y_probabilities = list(normiert.values())

    # Diagram ab hier:
    plot.stem(range(len(x_keys)), y_probabilities)
    for index, v in enumerate(y_probabilities):
        plot.text(index, v + 0.02, str(f"{v:.3f}"), ha='center')
    plot.xticks(range(len(x_keys)), x_keys)
    plot.ylim(0,1)
    plot.ylabel('P(X = x)')
    plot.title('Diskrete Wahrscheinlichkeitsverteilung')

    plot.show()