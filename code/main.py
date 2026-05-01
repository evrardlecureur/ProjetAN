# main.py
# Simulations, scénarios et visualisations de la cascade trophique.
#
# Structure :
#   0. Configuration générale
#   1. Simulation de base + comparaison des 4 solveurs (Figures 1 & 2)
#   2. Scénario Yellowstone : réintroduction des loups (Figures 3 & 4)
#   3. Analyse de convergence en norme L² (Figure 5)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from params import *
from model import F
from solvers import euler_explicite, euler_implicite, runge_kutta_4, crank_nicolson

# ======================================================================= #
#  0. Configuration générale                                               #
# ======================================================================= #

LABELS = ["Végétation $V$", "Wapitis $N$", "Cerfs $D$", "Loups $W$", "Ours $B$"]
UNITES = ["kg·km⁻²", "animaux·km⁻²", "animaux·km⁻²", "animaux·km⁻²", "animaux·km⁻²"]
COLORS = ["forestgreen", "steelblue", "cornflowerblue", "firebrick", "peru"]

t0 = 0.0   # an
tf = 50.0  # an
u0 = np.array([V0, N0, D0, W0, B0])

plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "--",
})


# ======================================================================= #
#  1. Simulation de base — tous les solveurs                               #
# ======================================================================= #

print("=" * 62)
print("1. SIMULATION DE BASE")
print("=" * 62)

# Justification des pas de temps (cohérente avec la section de Thibaud) :
#   RK4   h=0.005 an : référence de précision (ordre 4, très faible erreur)
#   Euler explicite h=0.005 an : conditionnellement stable, h doit rester petit
#   Euler implicite h=0.050 an : A-stable, pas plus grand autorisé
#   Crank-Nicolson  h=0.050 an : A-stable + ordre 2, meilleur compromis

h_rk4 = 0.005
h_exp  = 0.005
h_imp  = 0.050
h_cn   = 0.050

print(f"  RK4             h = {h_rk4} an  ({int(tf/h_rk4)} pas)")
print(f"  Euler explicite h = {h_exp} an  ({int(tf/h_exp)} pas)")
print(f"  Euler implicite h = {h_imp} an  ({int(tf/h_imp)} pas)")
print(f"  Crank-Nicolson  h = {h_cn}  an  ({int(tf/h_cn)} pas)")

t_rk4, U_rk4 = runge_kutta_4  (F, u0, t0, tf, h_rk4)
print("  ✓ RK4 terminé.")
t_exp, U_exp  = euler_explicite(F, u0, t0, tf, h_exp)
print("  ✓ Euler explicite terminé.")
t_imp, U_imp  = euler_implicite(F, u0, t0, tf, h_imp)
print("  ✓ Euler implicite terminé.")
t_cn,  U_cn   = crank_nicolson (F, u0, t0, tf, h_cn)
print("  ✓ Crank-Nicolson terminé.")

# ---------------------------------------------------------------------- #
#  Figure 1 — Évolution des 5 populations sur 50 ans (référence RK4)     #
# ---------------------------------------------------------------------- #

fig, axes = plt.subplots(5, 1, figsize=(11, 13), sharex=True)
fig.suptitle(
    "Cascade trophique — Simulation de référence sur 50 ans\n"
    r"(RK4, $h = 0{,}005$ an $\approx$ 1,8 jour)",
    fontsize=12, fontweight="bold", y=0.995
)

for i, (ax, label, unite, color) in enumerate(zip(axes, LABELS, UNITES, COLORS)):
    ax.plot(t_rk4, U_rk4[:, i], color=color, linewidth=1.5)
    ax.set_ylabel(unite, fontsize=9)
    ax.set_title(label, fontsize=11, loc="left", fontweight="bold", pad=4)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))

axes[-1].set_xlabel("Temps (années)", fontsize=11)
plt.tight_layout(rect=[0, 0, 1, 0.995])
plt.savefig("fig1_simulation_base.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✓ Figure 1 : fig1_simulation_base.png")

# ---------------------------------------------------------------------- #
#  Figure 2 — Comparaison des 4 solveurs                                 #
# ---------------------------------------------------------------------- #

solveurs_plot = [
    (t_rk4, U_rk4, f"RK4 ($h = {h_rk4}$ an)",             "black",       "-",  1.9, 0.95, 5),
    (t_exp, U_exp, f"Euler explicite ($h = {h_exp}$ an)",  "dodgerblue",  "--", 1.0, 0.85, 3),
    (t_imp, U_imp, f"Euler implicite ($h = {h_imp}$ an)",  "darkorange",  "-.", 1.0, 0.85, 3),
    (t_cn,  U_cn,  f"Crank-Nicolson ($h = {h_cn}$ an)",   "purple",      ":",  1.3, 0.85, 3),
]

fig, axes = plt.subplots(5, 1, figsize=(11, 13), sharex=True)
fig.suptitle(
    "Comparaison des solveurs numériques sur 50 ans",
    fontsize=12, fontweight="bold", y=0.995
)

for i, (ax, label, unite, color) in enumerate(zip(axes, LABELS, UNITES, COLORS)):
    for t_s, U_s, lbl, col, ls, lw, alpha, zorder in solveurs_plot:
        ax.plot(t_s, U_s[:, i], label=lbl, color=col, linestyle=ls,
                linewidth=lw, alpha=alpha, zorder=zorder)
    ax.set_title(label, fontsize=11, loc="left", fontweight="bold", pad=4)
    ax.set_ylabel(unite, fontsize=9)
    ax.legend(fontsize=7.5, loc="upper right", ncol=2, framealpha=0.6)

axes[-1].set_xlabel("Temps (années)", fontsize=11)
plt.tight_layout(rect=[0, 0, 1, 0.995])
plt.savefig("fig2_comparaison_solveurs.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✓ Figure 2 : fig2_comparaison_solveurs.png")


# ======================================================================= #
#  2. Scénario Yellowstone — Réintroduction des loups                      #
# ======================================================================= #

print()
print("=" * 62)
print("2. SCÉNARIO YELLOWSTONE")
print("=" * 62)

# Inspiré de la réintroduction des loups dans le parc de Yellowstone (1995).
#
# PROTOCOLE DE SIMULATION :
#   Phase 1 [0, t_reintr[ : absence totale de loups (W = 0 exactement).
#     Le vecteur u0_sans_loups = [V0, N0, D0, 0, B0] est un état valide
#     car dW/dt ∝ W : si W=0, les loups restent absents (équilibre trivial).
#     Sur cette période, la végétation est sur-pâturée et les ongulés
#     prolifèrent sans régulation par prédation.
#   Phase 2 [t_reintr, tf] : réintroduction de W_reintr loups/km².
#     Le dernier état de la Phase 1 sert de CI, avec W remplacé par W_reintr.
#     On observe alors la cascade trophique se mettre en place.
#
# On compare avec la simulation de référence (loups présents dès t=0).

t_reintr = 20.0   # an : année de réintroduction
W_reintr = 0.04   # animaux·km⁻² : même CI que la simulation de base
h_yellow = 0.01   # an : pas de temps (RK4, précis)

# Conditions initiales Phase 1 — écosystème sans loups
u0_phase1 = np.array([V0, N0, D0, 0.0, B0])

# Phase 1 : intégration sans loups
t1, U1 = runge_kutta_4(F, u0_phase1, t0, t_reintr, h_yellow)
print(f"  Phase 1 (sans loups, t ∈ [0, {int(t_reintr)}] an) terminée.")
print(f"    État final : V={U1[-1,0]:.1f} kg·km⁻²  "
      f"N={U1[-1,1]:.3f}  D={U1[-1,2]:.3f}  B={U1[-1,4]:.3f} animaux·km⁻²")
print(f"    → Végétation {'surpâturée' if U1[-1,0] < V0 else 'dense'} "
      f"({'−' if U1[-1,0] < V0 else '+'}{abs(U1[-1,0]-V0):.1f} kg·km⁻² par rapport aux CI de base)")
print(f"    → Wapitis : {'surnombre' if U1[-1,1] > N0 else 'déclin'} "
      f"({'+' if U1[-1,1] > N0 else ''}{U1[-1,1]-N0:.3f} animaux·km⁻²)")

# Conditions initiales Phase 2 = état final Phase 1 + loups réintroduits
u0_phase2    = U1[-1].copy()
u0_phase2[3] = W_reintr

# Phase 2 : intégration avec loups réintroduits
t2, U2 = runge_kutta_4(F, u0_phase2, t_reintr, tf, h_yellow)
print(f"  Phase 2 (loups réintroduits à t={int(t_reintr)} an) terminée.")
print(f"    État final : V={U2[-1,0]:.1f}  N={U2[-1,1]:.3f}  "
      f"D={U2[-1,2]:.3f}  W={U2[-1,3]:.4f}  B={U2[-1,4]:.3f}")

# Concaténation (on exclut le premier point de Phase 2 = déjà dans Phase 1)
t_yellow = np.concatenate([t1, t2[1:]])
U_yellow = np.concatenate([U1, U2[1:]], axis=0)

# Simulation de référence avec loups dès t=0 (même h pour comparaison équitable)
t_base, U_base = runge_kutta_4(F, u0, t0, tf, h_yellow)
print("  Simulation de référence (loups présents dès t=0) terminée.")

# ---------------------------------------------------------------------- #
#  Figure 3 — Yellowstone : évolution comparée des 5 populations          #
# ---------------------------------------------------------------------- #

fig, axes = plt.subplots(5, 1, figsize=(11, 13), sharex=True)
fig.suptitle(
    f"Scénario Yellowstone — Réintroduction des loups à $t = {int(t_reintr)}$ ans\n"
    r"(RK4, $h = 0{,}01$ an)",
    fontsize=12, fontweight="bold", y=0.995
)

for i, (ax, label, unite, color) in enumerate(zip(axes, LABELS, UNITES, COLORS)):
    ax.plot(t_base,   U_base[:, i],   color=color, lw=1.2, alpha=0.50,
            ls="--", label="Référence (loups présents dès $t = 0$)")
    ax.plot(t_yellow, U_yellow[:, i], color=color, lw=1.8,
            ls="-",  label=f"Yellowstone (réintroduction $t = {int(t_reintr)}$ ans)")
    ax.axvline(t_reintr, color="dimgray", ls=":", lw=1.0, alpha=0.7)
    ax.set_title(label, fontsize=11, loc="left", fontweight="bold", pad=4)
    ax.set_ylabel(unite, fontsize=9)
    ax.legend(fontsize=8, loc="upper right", framealpha=0.6)

# Annotation de la ligne de réintroduction sur le premier panneau
ylo, yhi = axes[0].get_ylim()
axes[0].text(
    t_reintr + 0.5, ylo + (yhi - ylo) * 0.10,
    f"Réintroduction\n$t = {int(t_reintr)}$ ans",
    fontsize=8, color="dimgray", va="bottom"
)

axes[-1].set_xlabel("Temps (années)", fontsize=11)
plt.tight_layout(rect=[0, 0, 1, 0.995])
plt.savefig("fig3_yellowstone.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✓ Figure 3 : fig3_yellowstone.png")

# ---------------------------------------------------------------------- #
#  Figure 4 — Portraits de phase N–W et D–W (progression temporelle)     #
# ---------------------------------------------------------------------- #
# Chaque point est coloré selon le temps (gradient viridis/plasma).
# Cela permet de visualiser la trajectoire de l'écosystème dans l'espace
# des états : spirale vers un attracteur, ou transient après réintroduction.

fig, axes = plt.subplots(2, 2, figsize=(11, 8))
fig.suptitle(
    "Portraits de phase — Dynamiques proie–prédateur",
    fontsize=12, fontweight="bold"
)

def phase_portrait(ax, X, Y, t_col, xlabel, ylabel, title, cmap="viridis"):
    sc = ax.scatter(X, Y, c=t_col, cmap=cmap, s=0.8, linewidths=0, zorder=2)
    ax.plot(X[0],  Y[0],  "go", ms=7, label="$t_0$",       zorder=5, clip_on=False)
    ax.plot(X[-1], Y[-1], "r*", ms=9, label="$t_f = 50$ ans", zorder=5, clip_on=False)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_title(title, fontsize=10, fontweight="bold")
    ax.legend(fontsize=8, loc="upper right", framealpha=0.6)
    plt.colorbar(sc, ax=ax, label="Temps (an)", pad=0.02, shrink=0.9)

phase_portrait(
    axes[0, 0],
    U_base[:, 1], U_base[:, 3], t_base,
    "Wapitis $N$ (animaux·km⁻²)", "Loups $W$ (animaux·km⁻²)",
    "Référence — $N$ vs $W$",
    cmap="viridis"
)
phase_portrait(
    axes[0, 1],
    U_yellow[:, 1], U_yellow[:, 3], t_yellow,
    "Wapitis $N$ (animaux·km⁻²)", "Loups $W$ (animaux·km⁻²)",
    f"Yellowstone — $N$ vs $W$ (réintro. $t = {int(t_reintr)}$ an)",
    cmap="plasma"
)
phase_portrait(
    axes[1, 0],
    U_base[:, 2], U_base[:, 3], t_base,
    "Cerfs $D$ (animaux·km⁻²)", "Loups $W$ (animaux·km⁻²)",
    "Référence — $D$ vs $W$",
    cmap="viridis"
)
phase_portrait(
    axes[1, 1],
    U_yellow[:, 2], U_yellow[:, 3], t_yellow,
    "Cerfs $D$ (animaux·km⁻²)", "Loups $W$ (animaux·km⁻²)",
    f"Yellowstone — $D$ vs $W$ (réintro. $t = {int(t_reintr)}$ an)",
    cmap="plasma"
)

plt.tight_layout()
plt.savefig("fig4_portraits_phase.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✓ Figure 4 : fig4_portraits_phase.png")


# ======================================================================= #
#  3. Analyse de convergence — ordre empirique des méthodes               #
# ======================================================================= #

print()
print("=" * 62)
print("3. ANALYSE DE CONVERGENCE")
print("=" * 62)

# On utilise RK4 avec un pas très fin comme solution de référence « exacte ».
# On intègre sur tf_conv an et on mesure l'erreur relative au point final :
#
#   e(h) = ||u_h(T) - u_ref(T)||_2 / ||u_ref(T)||_2
#
# Sur un graphe log-log, la pente donne l'ordre de convergence empirique :
# une droite de pente p signifie que e(h) ∝ h^p (méthode d'ordre p).

tf_conv    = 10.0     # an (durée courte pour que RK4 fin et méthodes d'ordre 1 restent fiables)
h_ref_conv = 5.0e-4   # an (RK4 à ce pas : erreur < 10⁻¹² en pratique)

print(f"  Solution de référence : RK4, h = {h_ref_conv} an sur T = {tf_conv} an...")
_, U_ref  = runge_kutta_4(F, u0, t0, tf_conv, h_ref_conv)
u_exact   = U_ref[-1]
print(f"    u_exact = [{', '.join(f'{x:.6f}' for x in u_exact)}]")

# Valeurs de h à tester — de fin (précis) à grossier
h_vals = np.array([0.002, 0.004, 0.008, 0.016, 0.032, 0.064])

err_exp, err_imp, err_cn, err_rk4 = [], [], [], []

print(f"\n  h (an)   | Euler exp  | Euler imp  | Crank-Nic  | RK4")
print(f"  {'-'*58}")

for h_test in h_vals:
    _, Ue = euler_explicite(F, u0, t0, tf_conv, h_test)
    _, Ui = euler_implicite(F, u0, t0, tf_conv, h_test)
    _, Uc = crank_nicolson (F, u0, t0, tf_conv, h_test)
    _, Ur = runge_kutta_4  (F, u0, t0, tf_conv, h_test)

    def rel_err(U_num):
        return np.linalg.norm(U_num[-1] - u_exact) / np.linalg.norm(u_exact)

    ee, ei, ec, er = rel_err(Ue), rel_err(Ui), rel_err(Uc), rel_err(Ur)
    err_exp.append(ee); err_imp.append(ei); err_cn.append(ec); err_rk4.append(er)
    print(f"  {h_test:.3f}    | {ee:.3e}  | {ei:.3e}  | {ec:.3e}  | {er:.3e}")

# Estimation des pentes empiriques (moindres carrés en log-log)
def slope(h_arr, err_arr):
    log_h  = np.log(h_arr)
    log_e  = np.log(err_arr)
    return np.polyfit(log_h, log_e, 1)[0]

p_exp  = slope(h_vals, err_exp)
p_imp  = slope(h_vals, err_imp)
p_cn   = slope(h_vals, err_cn)
p_rk4  = slope(h_vals, err_rk4)

print(f"\n  Ordres empiriques (pente log-log) :")
print(f"    Euler explicite  : {p_exp:.2f}  (théorique : 1)")
print(f"    Euler implicite  : {p_imp:.2f}  (théorique : 1)")
print(f"    Crank-Nicolson   : {p_cn:.2f}  (théorique : 2)")
print(f"    RK4              : {p_rk4:.2f}  (théorique : 4)")

# ---------------------------------------------------------------------- #
#  Figure 5 — Courbes de convergence (log-log)                            #
# ---------------------------------------------------------------------- #

h_arr = np.array(h_vals, dtype=float)

# Lignes de référence théoriques (ancrées au milieu de la plage de h)
mid = len(h_vals) // 2
scale1 = err_exp[mid] / h_vals[mid] ** 1
scale2 = err_cn [mid] / h_vals[mid] ** 2
scale4 = err_rk4[mid] / h_vals[mid] ** 4

fig, ax = plt.subplots(figsize=(8, 5.5))

ax.loglog(h_vals, err_exp,  "o-", color="dodgerblue", lw=1.8, ms=6,
          label=f"Euler explicite ($p \\approx {p_exp:.1f}$)")
ax.loglog(h_vals, err_imp,  "s-", color="darkorange",  lw=1.8, ms=6,
          label=f"Euler implicite ($p \\approx {p_imp:.1f}$)")
ax.loglog(h_vals, err_cn,   "^-", color="purple",      lw=1.8, ms=6,
          label=f"Crank-Nicolson ($p \\approx {p_cn:.1f}$)")
ax.loglog(h_vals, err_rk4,  "D-", color="firebrick",   lw=1.8, ms=6,
          label=f"RK4 ($p \\approx {p_rk4:.1f}$)")

ax.loglog(h_arr, scale1 * h_arr**1, "k--", alpha=0.30, lw=1.2,
          label=r"Pente $\mathcal{O}(h)$")
ax.loglog(h_arr, scale2 * h_arr**2, "k-.", alpha=0.30, lw=1.2,
          label=r"Pente $\mathcal{O}(h^2)$")
ax.loglog(h_arr, scale4 * h_arr**4, "k:",  alpha=0.30, lw=1.2,
          label=r"Pente $\mathcal{O}(h^4)$")

ax.set_xlabel("Pas de temps $h$ (années)", fontsize=11)
ax.set_ylabel(
    r"Erreur relative $\frac{\|\mathbf{u}_h(T) - \mathbf{u}_{\mathrm{ref}}(T)\|_2}"
    r"{\|\mathbf{u}_{\mathrm{ref}}(T)\|_2}$",
    fontsize=10
)
ax.set_title(
    f"Ordre de convergence des solveurs ($T = {int(tf_conv)}$ ans)",
    fontsize=12, fontweight="bold"
)
ax.legend(fontsize=8.5, loc="upper left", framealpha=0.7)
ax.grid(True, which="both", alpha=0.25, linestyle="--")
plt.tight_layout()
plt.savefig("fig5_convergence.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✓ Figure 5 : fig5_convergence.png")

# ======================================================================= #
#  Résumé final                                                            #
# ======================================================================= #

print()
print("=" * 62)
print("✅  Toutes les simulations sont terminées.")
print("   Figures générées :")
figs = [
    ("fig1", "Évolution de référence (RK4, 50 ans)"),
    ("fig2", "Comparaison des 4 solveurs"),
    ("fig3", "Scénario Yellowstone vs. référence"),
    ("fig4", "Portraits de phase N–W et D–W"),
    ("fig5", "Convergence en norme L² (log-log)"),
]
for i, (name, desc) in enumerate(figs, 1):
    print(f"   [{i}] {name}.png  — {desc}")
print("=" * 62)
