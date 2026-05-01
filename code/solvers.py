# solvers.py
# Solveurs numériques pour le système d'EDO.
# Chaque solveur prend en entrée :
#   - F      : fonction F(t, u) définie dans model.py
#   - u0     : vecteur d'état initial (numpy array)
#   - t0, tf : temps initial et final (en années)
#   - h      : pas de temps
#
# Implémentations [ROMAIN]  : euler_explicite
# Implémentations [THIBAUD] : euler_implicite, runge_kutta_4, crank_nicolson

import numpy as np


# ======================================================================= #
#  Utilitaire interne — Newton-Raphson vectoriel (à la main)               #
# ======================================================================= #

def _newton(G, u_guess, tol=1e-10, max_iter=50):
    """
    Résout G(u) = 0 par la méthode de Newton-Raphson.

    Le Jacobien J de G est approché colonne par colonne par différences
    finies centrées :

        J[:,j] ≈ [G(u + eps*e_j) - G(u - eps*e_j)] / (2*eps)

    où e_j est le j-ième vecteur de la base canonique et
    eps = sqrt(epsilon_machine) ≈ 1.5e-8.

    À chaque itération on résout le système linéaire J * delta = -G(u)
    via l'élimination gaussienne (np.linalg.solve), puis on met à jour
    u ← u + delta jusqu'à ||G(u)|| < tol.

    Paramètres
    ----------
    G        : callable, G(u) -> array de même taille que u
    u_guess  : point de départ (prédicteur Euler explicite en pratique)
    tol      : critère d'arrêt sur la norme de G(u)
    max_iter : nombre maximal d'itérations

    Retourne
    --------
    u : solution approchée de G(u) = 0
    """

    u   = u_guess.copy().astype(float)
    n   = len(u)
    eps = np.sqrt(np.finfo(float).eps)   # ≈ 1.49e-8

    for _ in range(max_iter):
        Gu = G(u)

        # Critère de convergence
        if np.linalg.norm(Gu) < tol:
            break

        # Construction du Jacobien colonne par colonne (différences finies centrées)
        J = np.zeros((n, n))
        for j in range(n):
            e_j     = np.zeros(n)
            e_j[j]  = eps
            J[:, j] = (G(u + e_j) - G(u - e_j)) / (2 * eps)

        # Résolution du système linéaire J * delta = -G(u)
        delta = np.linalg.solve(J, -Gu)
        u    += delta

    return u


# ======================================================================= #
#  [ROMAIN] — Euler explicite                                              #
# ======================================================================= #

def euler_explicite(F, u0, t0, tf, h):
    """
    Méthode d'Euler explicite.

    Schéma : u_{n+1} = u_n + h * F(t_n, u_n)

    C'est la méthode la plus simple : on approxime la dérivée au point
    actuel et on avance d'un pas h. Rapide à coder, mais conditionnellement
    stable — sur un système raide comme le nôtre, h doit rester très petit
    pour éviter que la solution explose.
    """

    t_values = np.arange(t0, tf + h, h)
    n_steps  = len(t_values)
    n_vars   = len(u0)

    U = np.zeros((n_steps, n_vars))
    U[0] = u0

    for n in range(n_steps - 1):
        U[n+1] = U[n] + h * F(t_values[n], U[n])

    return t_values, U


# ======================================================================= #
#  [THIBAUD] — Euler implicite                                             #
# ======================================================================= #

def euler_implicite(F, u0, t0, tf, h):
    """
    Méthode d'Euler implicite (Euler arrière).

    Schéma : u_{n+1} = u_n + h * F(t_{n+1}, u_{n+1})

    Contrairement à Euler explicite, la dérivée est évaluée au point
    *futur* t_{n+1}, ce qui rend le schéma inconditionnellement stable
    (A-stable). C'est essentiel pour un système raide comme le nôtre :
    on peut utiliser un pas h bien plus grand sans instabilité numérique.

    Chaque pas nécessite de résoudre le système non linéaire :

        G(u_{n+1}) = u_{n+1} - u_n - h * F(t_{n+1}, u_{n+1}) = 0

    On utilise notre Newton-Raphson (_newton) avec comme prédicteur le
    pas Euler explicite : u_guess = u_n + h * F(t_n, u_n).

    Coût par pas : ~4n évaluations de F par itération Newton (n=5 ici),
    convergence en ≈ 3–6 itérations en pratique.
    """

    t_values = np.arange(t0, tf + h, h)
    n_steps  = len(t_values)
    n_vars   = len(u0)

    U = np.zeros((n_steps, n_vars))
    U[0] = u0

    for n in range(n_steps - 1):
        t_next = t_values[n + 1]
        u_n    = U[n]

        def G(u_next):
            return u_next - u_n - h * F(t_next, u_next)

        u_guess  = u_n + h * F(t_values[n], u_n)   # prédicteur Euler explicite
        U[n + 1] = _newton(G, u_guess)

    return t_values, U


# ======================================================================= #
#  [THIBAUD] — Runge-Kutta d'ordre 4 (RK4)                                #
# ======================================================================= #

def runge_kutta_4(F, u0, t0, tf, h):
    """
    Méthode de Runge-Kutta d'ordre 4 (RK4 classique).

    Schéma à 4 étages :
        k1 = F(t_n,         u_n)
        k2 = F(t_n + h/2,   u_n + h/2 * k1)
        k3 = F(t_n + h/2,   u_n + h/2 * k2)
        k4 = F(t_n + h,     u_n + h   * k3)

        u_{n+1} = u_n + h/6 * (k1 + 2*k2 + 2*k3 + k4)

    Méthode explicite d'ordre 4 : l'erreur de troncature locale est en
    O(h^5), ce qui permet d'utiliser des pas plus grands qu'Euler explicite
    tout en gardant une bien meilleure précision.

    Sert de référence de précision pour valider Euler implicite et
    Crank-Nicolson.

    Coût par pas : 4 évaluations de F (contre 1 pour Euler).
    """

    t_values = np.arange(t0, tf + h, h)
    n_steps  = len(t_values)
    n_vars   = len(u0)

    U = np.zeros((n_steps, n_vars))
    U[0] = u0

    for n in range(n_steps - 1):
        t_n = t_values[n]
        u_n = U[n]

        k1 = F(t_n,         u_n)
        k2 = F(t_n + h / 2, u_n + h / 2 * k1)
        k3 = F(t_n + h / 2, u_n + h / 2 * k2)
        k4 = F(t_n + h,     u_n + h       * k3)

        U[n + 1] = u_n + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

    return t_values, U


# ======================================================================= #
#  [THIBAUD] — Crank-Nicolson (trapèze implicite)                         #
# ======================================================================= #

def crank_nicolson(F, u0, t0, tf, h):
    """
    Méthode de Crank-Nicolson (règle du trapèze implicite).

    Schéma : u_{n+1} = u_n + h/2 * [F(t_n, u_n) + F(t_{n+1}, u_{n+1})]

    Méthode d'ordre 2, A-stable, symétrique en temps.
    Elle combine la stabilité inconditionnelle d'Euler implicite avec une
    précision au second ordre — meilleure qu'Euler implicite (ordre 1)
    pour un coût identique par pas.

    Système non linéaire à résoudre à chaque pas :

        G(u_{n+1}) = u_{n+1} - u_n - h/2 * (F_n + F(t_{n+1}, u_{n+1})) = 0

    F_n = F(t_n, u_n) est calculé une seule fois et capturé dans la
    closure de G. Prédicteur : Euler explicite.

    Justification : la raideur de notre système vient des oscillations
    saisonnières (T = 1 an) et de la végétation. Crank-Nicolson converge
    avec h = 0.05 (20 pas/an) sans instabilité, là où Euler explicite
    exige h ≤ 0.01.
    """

    t_values = np.arange(t0, tf + h, h)
    n_steps  = len(t_values)
    n_vars   = len(u0)

    U = np.zeros((n_steps, n_vars))
    U[0] = u0

    for n in range(n_steps - 1):
        t_n    = t_values[n]
        t_next = t_values[n + 1]
        u_n    = U[n]
        F_n    = F(t_n, u_n)   # calculé une seule fois, capturé dans la closure

        def G(u_next):
            return u_next - u_n - (h / 2) * (F_n + F(t_next, u_next))

        u_guess  = u_n + h * F_n   # prédicteur Euler explicite
        U[n + 1] = _newton(G, u_guess)

    return t_values, U
