"""This will be a simulation for a general scenario in video games that include critical hits, 
we can define a function that calculates the damage dealt by an attack considering the possibility of a critical hit.
There are two 'stats' that are important: Critical Hit Chance (CC) which has a natural cap of 100% and Critical Hit Damage (CD) which caps at 300%.
CC is the probability (in percentage) that an attack will be a critical hit, while CD is the multiplier applied to the damage when a critical hit occurs.
This code shall provide insight into where sweetspots or breakpoints lie for maximizing 'Damage per Second' (DPS) based on varying CC and CD values.
This code will prompt the user to input two iterations of values for CC and CD, simulates the damage output over a fixed period and then compares the two sets/iterations of values.
Ideally in the end we get a graph or a table that shows how different combinations of CC and CD affect overall damage output."""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to calculate expected damage per hit
def expected_damage(base_damage, crit_chance, crit_damage):
    crit_multiplier = 1 + (crit_damage / 100)
    # Expected damage = normal damage (non-crit) + critical damage
    expected_dmg = base_damage * ((1 - crit_chance / 100) + crit_multiplier * (crit_chance / 100))
    return expected_dmg

# Simulation parameters
base_damage = 1000  # Base damage per hit
attack_speed = 1.0  # Attacks per second
simulation_time = 120  # Total simulation time in seconds
time_steps = int(simulation_time * attack_speed)

crit_chances = np.arange(0, 101, 2)  # Critical hit chances from 0% to 100%
crit_damages = np.arange(0, 301, 5)  # Critical hit damages from 0% to 300%
dps_results = np.zeros((len(crit_chances), len(crit_damages)))

# Run simulation
for i, cc in enumerate(crit_chances):
    for j, cd in enumerate(crit_damages):
        dmg_per_hit = expected_damage(base_damage, cc, cd)
        total_damage = dmg_per_hit * time_steps
        dps = total_damage / simulation_time
        dps_results[i, j] = dps

# Plotting the results
# 1. Heatmap visualization
plt.figure(figsize=(12, 8))
X, Y = np.meshgrid(crit_damages, crit_chances)
contour = plt.contourf(X, Y, dps_results, levels=20, cmap='viridis')
plt.colorbar(contour, label='DPS')
plt.xlabel('Critical Hit Damage (%)')
plt.ylabel('Critical Hit Chance (%)')
plt.title('Damage Per Second (DPS) vs Critical Hit Chance and Damage')
plt.tight_layout()
plt.savefig('dps_heatmap.png')  # Save as image
plt.show()

# 2. 3D Surface plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, dps_results, cmap='viridis')
ax.set_xlabel('Critical Hit Damage (%)')
ax.set_ylabel('Critical Hit Chance (%)')
ax.set_zlabel('DPS')
ax.set_title('3D DPS Surface')
plt.savefig('dps_3d_surface.png')  # Save as image
plt.show()

# 3. Print max DPS and optimal values
max_dps_idx = np.unravel_index(np.argmax(dps_results), dps_results.shape)
optimal_cc = crit_chances[max_dps_idx[0]]
optimal_cd = crit_damages[max_dps_idx[1]]
max_dps = dps_results[max_dps_idx]

print(f"\nOptimal values:")
print(f"Critical Hit Chance: {optimal_cc}%")
print(f"Critical Hit Damage: {optimal_cd}%")
print(f"Maximum DPS: {max_dps:.2f}")