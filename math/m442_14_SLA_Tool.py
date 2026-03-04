# Aufgabe 14: Wie lässt sich ein digitales Tool konstruieren, 
# das die Wahrscheinlichkeit für das Reißen von SLAs automatisiert prognostiziert?

#import matplotlib.pyplot as plot
import random as rd

# Hardcoding Test Data
messtage = 10
messungen_pro_std = 60
messungen_pro_tag = 24 * messungen_pro_std
messungen_gesamt = messtage * messungen_pro_tag

# Definition Rahmen, ping über 1000ms -> 'disconnect'/Fehlschlag
sla_limit = 99.5
threshold = 1000
sla_zeitraum = 365
max_fails: int = int((100 - sla_limit) / 100 * (messungen_pro_tag * sla_zeitraum))

# Simulation
GRADES = [1, 2]
WEIGHTS = [99.5, 0.5]
sim_pings = []

def sim_ping(grade):
    if grade == 1:
        return rd.randint(0, 900)
    elif grade == 2:
        return rd.randint(901, 5000)
    else: return 0

for m in range(messungen_gesamt):
    weighted_choice = rd.choices(GRADES, weights=WEIGHTS, k=1)[0]
    sim_pings.append(sim_ping(weighted_choice))

# Basiswerte berechnen
mw_ping = sum(sim_pings) / messungen_gesamt
max_ping = max(sim_pings)
min_ping = min(sim_pings)
fails = sum(1 for m in sim_pings if m > threshold)
# Weitergehende Rechnungen (Prognosen)
verbleibende_tage = sla_zeitraum - messtage
n = verbleibende_tage * messungen_pro_tag
p = fail_probability = fails / len(sim_pings)
fehler_budget: int = int(max_fails - fails)
# Komplexer (Normalverteilung)
import math

def normal_cdf(x, mu, sigma):
    # Approximation des Fehlers (Error Function erf)
    return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))

# Erwartungswert und Standardabweichung
erwartungswert = n * p
std_abw = math.sqrt(n * p * (1 - p))

# Risiko berechnen
# Wir wollen wissen: P(X > budget)
# Das ist 1 - P(X <= budget)
if std_abw > 0:
    prob_within_budget = normal_cdf(fehler_budget, erwartungswert, std_abw)
    risk_of_breach = 1 - prob_within_budget
else:
    risk_of_breach = 1.0 if fehler_budget < 0 else 0.0

print(f"Risiko d. SLA-Bruchs: {risk_of_breach:.4%}")
