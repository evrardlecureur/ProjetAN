# solvers.py - solveurs numériques pour notre système d'EDO
# Romain : euler_explicite
# Thibaud : le reste

import numpy as np


def _newton(G, u_guess, tol=1e-10, max_iter=50):
    """
    Newton-Raphson pour résoudre G(u) = 0.
    On approche le jacobien par différences finies centrées.
    """
    u   = u_guess.copy().astype(float)
    n   = len(u)
    eps = np.sqrt(np.finfo(float).eps)

    for _ in range(max_iter):
        Gu = G(u)
        if np.linalg.norm(Gu) < tol:
            break
        # jacobien colonne par colonne
        J = np.zeros((n, n))
        for j in range(n):
            ej      = np.zeros(n)
            ej[j]   = eps
            J[:, j] = (G(u + ej) - G(u - ej)) / (2 * eps)
        delta = np.linalg.solve(J, -Gu)
        u += delta

    return u


def euler_explicite(F, u0, t0, tf, h):
    """
    Euler explicite : u_{n+1} = u_n + h * F(t_n, u_n)
    Simple mais conditionnellement stable, h doit rester petit
    sur un système raide comme le nôtre.
    """
    t_vals = np.arange(t0, tf + h, h)
    U = np.zeros((len(t_vals), len(u0)))
    U[0] = u0

    for n in range(len(t_vals) - 1):
        U[n+1] = U[n] + h * F(t_vals[n], U[n])

    return t_vals, U


def euler_implicite(F, u0, t0, tf, h):
    """
    Euler implicite : u_{n+1} = u_n + h * F(t_{n+1}, u_{n+1})
    u_{n+1} est inconnu des deux côtés donc on résout
    G(u_{n+1}) = 0 avec Newton à chaque pas.
    A-stable => pas h plus grand possible sans instabilité.
    """
    t_vals = np.arange(t0, tf + h, h)
    U = np.zeros((len(t_vals), len(u0)))
    U[0] = u0

    for n in range(len(t_vals) - 1):
        t_next = t_vals[n + 1]
        u_n    = U[n]

        def G(u_next):
            return u_next - u_n - h * F(t_next, u_next)

        # prédicteur = Euler explicite pour démarrer Newton
        u_guess  = u_n + h * F(t_vals[n], u_n)
        U[n + 1] = _newton(G, u_guess)

    return t_vals, U


def runge_kutta_4(F, u0, t0, tf, h):
    """
    RK4 classique : 4 évaluations de F par pas, ordre 4.
    Sert de référence "quasi-exacte" pour la comparaison.
    """
    t_vals = np.arange(t0, tf + h, h)
    U = np.zeros((len(t_vals), len(u0)))
    U[0] = u0

    for n in range(len(t_vals) - 1):
        tn  = t_vals[n]
        un  = U[n]
        k1  = F(tn,         un)
        k2  = F(tn + h/2,   un + h/2 * k1)
        k3  = F(tn + h/2,   un + h/2 * k2)
        k4  = F(tn + h,     un + h   * k3)
        U[n+1] = un + (h/6) * (k1 + 2*k2 + 2*k3 + k4)

    return t_vals, U


def crank_nicolson(F, u0, t0, tf, h):
    """
    Crank-Nicolson : u_{n+1} = u_n + h/2 * (F_n + F_{n+1})
    Ordre 2 et A-stable, meilleur compromis précision/stabilité.
    """
    t_vals = np.arange(t0, tf + h, h)
    U = np.zeros((len(t_vals), len(u0)))
    U[0] = u0

    for n in range(len(t_vals) - 1):
        t_n    = t_vals[n]
        t_next = t_vals[n + 1]
        u_n    = U[n]
        Fn     = F(t_n, u_n)

        def G(u_next):
            return u_next - u_n - (h/2) * (Fn + F(t_next, u_next))

        u_guess  = u_n + h * Fn
        U[n + 1] = _newton(G, u_guess)

    return t_vals, U
