# main.py
# Point d'entrée du projet. Lance la simulation et affiche les graphiques.
# Zhouair : c'est ici que tu travailleras pour les simulations et le scénario Yellowstone.

import numpy as np
import matplotlib.pyplot as plt

from params import *
from model import F
from solvers import euler_explicite

# ------------------------------------------------------------------ #
# Paramètres de simulation
# ------------------------------------------------------------------ #

t0 = 0.0    # année de départ
tf = 50.0   # durée de simulation (années)
h  = 0.01   # pas de temps (en années, ~3.6 jours)
              # Sur un système raide, h doit rester petit avec Euler explicite.

u0 = np.array([V0, N0, D0, W0, B0])  # conditions initiales (params.py)

# ------------------------------------------------------------------ #
# Lancement de la simulation
# ------------------------------------------------------------------ #

t_vals, U = euler_explicite(F, u0, t0, tf, h)

# Extraction de chaque population
V_sol = U[:, 0]
N_sol = U[:, 1]
D_sol = U[:, 2]
W_sol = U[:, 3]
B_sol = U[:, 4]

# ------------------------------------------------------------------ #
# Visualisation
# ------------------------------------------------------------------ #

fig, axes = plt.subplots(5, 1, figsize=(12, 14), sharex=True)
fig.suptitle("Cascade trophique — Simulation sur 50 ans", fontsize=14, fontweight='bold')

donnees = [
    (V_sol, "Végétation V",            "kg·km⁻²",        "forestgreen"),
    (N_sol, "Wapitis/Orignaux N",       "animaux·km⁻²",   "steelblue"),
    (D_sol, "Cerfs D",                  "animaux·km⁻²",   "cornflowerblue"),
    (W_sol, "Loups W",                  "animaux·km⁻²",   "firebrick"),
    (B_sol, "Ours B",                   "animaux·km⁻²",   "peru"),
]

for ax, (data, label, unite, couleur) in zip(axes, donnees):
    ax.plot(t_vals, data, color=couleur, linewidth=1.2)
    ax.set_ylabel(unite, fontsize=9)
    ax.set_title(label, fontsize=10, loc='left')
    ax.grid(True, alpha=0.3)

axes[-1].set_xlabel("Temps (années)", fontsize=11)
plt.tight_layout()
plt.savefig("simulation_base.png", dpi=150)
plt.show()
