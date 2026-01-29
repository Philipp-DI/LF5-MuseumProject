/* This will be a simulation for a general scenario in video games that include critical hits, 
we can define a function that calculates the damage dealt by an attack considering the possibility of a critical hit.
There are two 'stats' that are important: Critical Hit Chance (CC) which has a natural cap of 100% and Critical Hit Damage (CD) which caps at 300%.
CC is the probability (in percentage) that an attack will be a critical hit, while CD is the multiplier applied to the damage when a critical hit occurs.
This code shall provide insight into where sweetspots or breakpoints lie for maximizing 'Damage per Second' (DPS) based on varying CC and CD values.
This code will simulate 120 seconds of combat, assuming a fixed attack speed and base damage.
Ideally in the end we get a graph or a table that shows how different combinations of CC and CD affect overall damage output.*/

// const np = require('numpy');
// const plt = require('matplotlib.pyplot');

// Function to calculate expected damage per hit
function expected_damage(base_damage, crit_chance, crit_damage) {
    const crit_multiplier = 1 + (crit_damage / 100);
    const expected_dmg = (base_damage * (1 - crit_chance / 100)) + (base_damage * crit_multiplier * (crit_chance / 100));
    return expected_dmg;
}
// Simulation parameters
const base_damage = 1000;  // Base damage per hit
const attack_speed = 1.0;  // Attacks per second
const simulation_time = 120;  // Total simulation time in seconds
const time_steps = Math.floor(simulation_time * attack_speed);
const crit_chances = [];
for (let cc = 0; cc <= 100; cc += 2) crit_chances.push(cc);  // Critical hit chances from 0% to 100%
const crit_damages = [];
for (let cd = 0; cd <= 300; cd += 5) crit_damages.push(cd);  // Critical hit damages from 0% to 300%
const dps_results = Array.from({ length: crit_chances.length }, () => Array(crit_damages.length).fill(0));

// Run simulation
for (let i = 0; i < crit_chances.length; i++) {
    const cc = crit_chances[i];
    for (let j = 0; j < crit_damages.length; j++) {
        const cd = crit_damages[j];
        const dmg_per_hit = expected_damage(base_damage, cc, cd);
        const total_damage = dmg_per_hit * time_steps;
        const dps = total_damage / simulation_time;
        dps_results[i][j] = dps;
    }
}

// Plotting the results
// Visualization is not implemented in this JavaScript version.
// You can output the dps_results as a table or use a JS plotting library like Chart.js or Plotly for visualization.
console.log("DPS Results Table:");
console.table(dps_results);

//Visualization
// const X = np.array(crit_damages);
// const Y = np.array(crit_chances);
// const Z = np.array(dps_results);