import matplotlib.pyplot as plot
import seaborn as sb

CHANCES = {
    'Blau': 0.870,
    'Violett': 0.128,
    'Gold': 0.002
}

gesamt_p = 0
for k, p in CHANCES.items():
    gesamt_p += p
    
