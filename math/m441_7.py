import statistics as stats
import datetime as dt

class Schadensszenario:
    def __init__(self, titel: str, schadenssumme: float, wahrscheinlichkeit: float):
        self.titel = titel
        self.schadenssumme = schadenssumme
        self.prob = wahrscheinlichkeit
        self.added_date = dt.datetime.now().strftime("%Y-%m-%d")
        self.expected_dmg = self.schadenssumme * self.prob
        
        
    @staticmethod
    def statistik():
        mw_schaden = stats.fmean(s.schadenssumme for s in all_data)
        med_schaden = stats.median(s.schadenssumme for s in all_data)
        sum_expected_dmg = sum(s.expected_dmg for s in all_data)
        mw_prob = stats.fmean(s.prob for s in all_data)
        total = sum(s.schadenssumme for s in all_data)
        return mw_schaden, med_schaden, sum_expected_dmg, mw_prob, total
    
    @classmethod
    def anzeige(cls):
        mw, med, sum_e, mw_p, total = cls.statistik()
        print(f"Gesamtanzahl der Szenarios: {len(all_data)}\n")
        print(f"{'Event':<14} | {'Schadenssumme':^15} | {'P':^6} | {'Erwartungswert':^16} | {'Anteil am erwarteten Gesamtschaden':>20}")
        print('='*100)
        for s in all_data:
            print(f"{s.titel:<14} | {s.schadenssumme:>13} € | {s.prob:>6.1%} | {s.expected_dmg:>14.2f} € | {s.expected_dmg / sum_e:<20.2%}")
        print('-'*100)
        print(f"{'Gesamt:':<14} | {total:>13} € | {sum(s.prob for s in all_data):>6.1%} | {sum_e:>14.2f} € | {sum((s.expected_dmg / sum_e) for s in all_data):<20.2%}\n")
        
        print(f"{'Mittelwerte & Co:'} MW Gesamtschaden: {mw:.2f} €, MED: {med:.2f} € | MW Wahrscheinlichkeiten: {mw_p:.1%} | MW zu erwartender Schaden: {stats.fmean(s.expected_dmg for s in all_data):.2f} €")

# Szenarios, Wahrscheinlichkeiten stellen 1 Fall pro Jahr dar:
data = [
    {'titel': 'Sturm', 'schadenssumme': 4000, 'wahrscheinlichkeit': 0.4},
    {'titel': 'Diebstahl', 'schadenssumme': 800, 'wahrscheinlichkeit': 1},
    {'titel': 'Vandalismus', 'schadenssumme': 2000, 'wahrscheinlichkeit': 0.6},
    {'titel': 'Data Breach', 'schadenssumme': 500000, 'wahrscheinlichkeit': 0.08},
    {'titel': 'Brand', 'schadenssumme': 7000, 'wahrscheinlichkeit': 0.1},
    {'titel': 'Großbrand', 'schadenssumme': 14000, 'wahrscheinlichkeit': 0.004},
    {'titel': 'Hagelschaden', 'schadenssumme': 600, 'wahrscheinlichkeit': 0.7},
    {'titel': 'Unfall', 'schadenssumme': 5000, 'wahrscheinlichkeit': 0.8},
    {'titel': 'Stromausfall', 'schadenssumme': 2000, 'wahrscheinlichkeit': 0.3},
    {'titel': 'Erdbeben', 'schadenssumme': 100000, 'wahrscheinlichkeit': 0.002}
    ]
all_data = []
for scenario in data:
    all_data.append(Schadensszenario(**scenario))
Schadensszenario.anzeige()
