# main.py - simulations et graphiques
# scénarios : base + Yellowstone + convergence

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from params import *
from model import F
from solvers import euler_explicite, euler_implicite, runge_kutta_4, crank_nicolson

# labels et couleurs pour les graphiques
LABELS = ["Végétation V", "Wapitis N", "Cerfs D", "Loups W", "Ours B"]
UNITES = ["kg·km⁻²", "animaux·km⁻²", "animaux·km⁻²", "animaux·km⁻²", "animaux·km⁻²"]
COLORS = ["forestgreen", "steelblue", "cornflowerblue", "firebrick", "peru"]

t0 = 0.0
tf = 50.0
u0 = np.array([V0, N0, D0, W0, B0])

# ------------------------------------------------------------------ #
# 1. Simulation de base — comparaison des 4 solveurs
# ------------------------------------------------------------------ #
# On choisit h plus petit pour Euler explicite car il est conditionnellement
# stable, et h plus grand pour les méthodes implicites (A-stables).

h_rk4 = 0.005
h_exp  = 0.005
h_imp  = 0.050
h_cn   = 0.050

t_rk4, U_rk4 = runge_kutta_4  (F, u0, t0, tf, h_rk4)
t_exp, U_exp  = euler_explicite(F, u0, t0, tf, h_exp)
t_imp, U_imp  = euler_implicite(F, u0, t0, tf, h_imp)
t_cn,  U_cn   = crank_nicolson (F, u0, t0, tf, h_cn)

# Figure 1 : évolution de référence (RK4)
fig, axes = plt.subplots(5, 1, figsize=(11, 13), sharex=True)
fig.suptitle("Cascade trophique — Simulation de référence sur 50 ans (RK4)", fontsize=12)

for i, (ax, label, unite, color) in enumerate(zip(axes, LABELS, UNITES, COLORS)):
    ax.plot(t_rk4, U_rk4[:, i], color=color, lw=1.5)
    ax.set_ylabel(unite, fontsize=9)
    ax.set_title(label, fontsize=11, loc="left")
    ax.grid(alpha=0.25)

axes[-1].set_xlabel("Temps (années)")
plt.tight_layout()
plt.savefig("fig1_simulation_base.png", dpi=150, bbox_inches="tight")
plt.close()

# Figure 2 : comparaison des 4 solveurs
solveurs = [
    (t_rk4, U_rk4, f"RK4 (h={h_rk4})",             "black",      "-",  1.8),
    (t_exp, U_exp, f"Euler explicite (h={h_exp})",  "dodgerblue", "--", 1.0),
    (t_imp, U_imp, f"Euler implicite (h={h_imp})",  "darkorange", "-.", 1.0),
    (t_cn,  U_cn,  f"Crank-Nicolson (h={h_cn})",   "purple",     ":",  1.3),
]

fig, axes = plt.subplots(5, 1, figsize=(11, 13), sharex=True)
fig.suptitle("Comparaison des solveurs sur 50 ans", fontsize=12)

for i, (ax, label, unite, color) in enumerate(zip(axes, LABELS, UNITES, COLORS)):
    for t_s, U_s, lbl, col, ls, lw in solveurs:
        ax.plot(t_s, U_s[:, i], label=lbl, color=col, ls=ls, lw=lw, alpha=0.85)
    ax.set_title(label, fontsize=11, loc="left")
    ax.set_ylabel(unite, fontsize=9)
    ax.legend(fontsize=7.5, loc="upper right", ncol=2, framealpha=0.6)
    ax.grid(alpha=0.25)

axes[-1].set_xlabel("Temps (années)")
plt.tight_layout()
plt.savefig("fig2_comparaison_solveurs.png", dpi=150, bbox_inches="tight")
plt.close()

# ------------------------------------------------------------------ #
# 2. Scénario Yellowstone
# ------------------------------------------------------------------ #
# Phase 1 : pas de loups du tout (W=0)
# Phase 2 : on réintroduit des loups à t_reintr

t_reintr = 20.0
W_reintr = 0.04
h_y      = 0.01

u0_sans_loups = np.array([V0, N0, D0, 0.0, B0])

t1, U1 = runge_kutta_4(F, u0_sans_loups, t0, t_reintr, h_y)

# état final de la phase 1 + réintroduction
u0_phase2    = U1[-1].copy()
u0_phase2[3] = W_reintr

t2, U2 = runge_kutta_4(F, u0_phase2, t_reintr, tf, h_y)

# on colle les deux phases
t_yellow = np.concatenate([t1, t2[1:]])
U_yellow = np.concatenate([U1, U2[1:]], axis=0)

# simulation de référence pour comparaison
t_base, U_base = runge_kutta_4(F, u0, t0, tf, h_y)

# Figure 3 : Yellowstone
fig, axes = plt.subplots(5, 1, figsize=(11, 13), sharex=True)
fig.suptitle(f"Scénario Yellowstone — réintroduction des loups à t={int(t_reintr)} ans", fontsize=12)

for i, (ax, label, unite, color) in enumerate(zip(axes, LABELS, UNITES, COLORS)):
    ax.plot(t_base,   U_base[:, i],   color=color, lw=1.2, ls="--", alpha=0.5,
            label="loups présents dès t=0")
    ax.plot(t_yellow, U_yellow[:, i], color=color, lw=1.8,
            label=f"réintroduction à t={int(t_reintr)} ans")
    ax.axvline(t_reintr, color="gray", ls=":", lw=1.0)
    ax.set_title(label, fontsize=11, loc="left")
    ax.set_ylabel(unite, fontsize=9)
    ax.legend(fontsize=8, loc="upper right", framealpha=0.6)
    ax.grid(alpha=0.25)

axes[-1].set_xlabel("Temps (années)")
plt.tight_layout()
plt.savefig("fig3_yellowstone.png", dpi=150, bbox_inches="tight")
plt.close()

# Figure 4 : portraits de phase N-W et D-W
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
fig.suptitle("Portraits de phase — dynamiques proie–prédateur", fontsize=12)

def phase_portrait(ax, X, Y, t_col, xlabel, ylabel, title, cmap="viridis"):
    sc = ax.scatter(X, Y, c=t_col, cmap=cmap, s=0.8)
    ax.plot(X[0],  Y[0],  "go", ms=7, label="t=0")
    ax.plot(X[-1], Y[-1], "r*", ms=9, label="t=50 ans")
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=8)
    plt.colorbar(sc, ax=ax, label="Temps (an)", shrink=0.9)

phase_portrait(axes[0,0], U_base[:,1],   U_base[:,3],   t_base,
               "Wapitis N", "Loups W", "Référence — N vs W")
phase_portrait(axes[0,1], U_yellow[:,1], U_yellow[:,3], t_yellow,
               "Wapitis N", "Loups W", f"Yellowstone — N vs W", cmap="plasma")
phase_portrait(axes[1,0], U_base[:,2],   U_base[:,3],   t_base,
               "Cerfs D", "Loups W", "Référence — D vs W")
phase_portrait(axes[1,1], U_yellow[:,2], U_yellow[:,3], t_yellow,
               "Cerfs D", "Loups W", f"Yellowstone — D vs W", cmap="plasma")

plt.tight_layout()
plt.savefig("fig4_portraits_phase.png", dpi=150, bbox_inches="tight")
plt.close()

# ------------------------------------------------------------------ #
# 3. Analyse de convergence
# ------------------------------------------------------------------ #
# On prend RK4 avec h très fin comme solution de référence
# et on mesure l'erreur relative au point final pour différentes valeurs de h.
# Sur un graphe log-log la pente = ordre empirique de la méthode.

tf_conv = 10.0
h_ref   = 5e-4

_, U_ref = runge_kutta_4(F, u0, t0, tf_conv, h_ref)
u_exact  = U_ref[-1]

h_vals = [0.002, 0.004, 0.008, 0.016, 0.032, 0.064]
err_exp, err_imp, err_cn, err_rk4 = [], [], [], []

for h_test in h_vals:
    _, Ue = euler_explicite(F, u0, t0, tf_conv, h_test)
    _, Ui = euler_implicite(F, u0, t0, tf_conv, h_test)
    _, Uc = crank_nicolson (F, u0, t0, tf_conv, h_test)
    _, Ur = runge_kutta_4  (F, u0, t0, tf_conv, h_test)

    def err(U):
        return np.linalg.norm(U[-1] - u_exact) / np.linalg.norm(u_exact)

    err_exp.append(err(Ue))
    err_imp.append(err(Ui))
    err_cn.append(err(Uc))
    err_rk4.append(err(Ur))

# estimation des ordres par moindres carrés en log-log
def ordre(hs, errs):
    return np.polyfit(np.log(hs), np.log(errs), 1)[0]

h_arr  = np.array(h_vals)
p_exp  = ordre(h_arr, err_exp)
p_imp  = ordre(h_arr, err_imp)
p_cn   = ordre(h_arr, err_cn)
p_rk4  = ordre(h_arr, err_rk4)

print(f"Ordres empiriques :")
print(f"  Euler explicite : {p_exp:.2f}  (théorique : 1)")
print(f"  Euler implicite : {p_imp:.2f}  (théorique : 1)")
print(f"  Crank-Nicolson  : {p_cn:.2f}   (théorique : 2)")
print(f"  RK4             : {p_rk4:.2f}  (théorique : 4)")

# Figure 5 : convergence log-log
mid    = len(h_vals) // 2
s1     = err_exp[mid] / h_vals[mid] ** 1
s2     = err_cn[mid]  / h_vals[mid] ** 2
s4     = err_rk4[mid] / h_vals[mid] ** 4

fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(h_vals, err_exp,  "o-", color="dodgerblue", lw=1.8, ms=6,
          label=f"Euler explicite (p≈{p_exp:.1f})")
ax.loglog(h_vals, err_imp,  "s-", color="darkorange",  lw=1.8, ms=6,
          label=f"Euler implicite (p≈{p_imp:.1f})")
ax.loglog(h_vals, err_cn,   "^-", color="purple",      lw=1.8, ms=6,
          label=f"Crank-Nicolson (p≈{p_cn:.1f})")
ax.loglog(h_vals, err_rk4,  "D-", color="firebrick",   lw=1.8, ms=6,
          label=f"RK4 (p≈{p_rk4:.1f})")
ax.loglog(h_arr, s1 * h_arr**1, "k--", alpha=0.3, lw=1.2, label="O(h)")
ax.loglog(h_arr, s2 * h_arr**2, "k-.", alpha=0.3, lw=1.2, label="O(h²)")
ax.loglog(h_arr, s4 * h_arr**4, "k:",  alpha=0.3, lw=1.2, label="O(h⁴)")
ax.set_xlabel("Pas de temps h (années)")
ax.set_ylabel("Erreur relative L²")
ax.set_title(f"Ordre de convergence (T={int(tf_conv)} ans)")
ax.legend(fontsize=8.5, loc="upper left", framealpha=0.7)
ax.grid(True, which="both", alpha=0.25, ls="--")
plt.tight_layout()
plt.savefig("fig5_convergence.png", dpi=150, bbox_inches="tight")
plt.close()

print("Toutes les figures générées.")
