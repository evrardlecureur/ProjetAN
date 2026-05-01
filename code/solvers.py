# solvers.py
# Solveurs numériques pour le système d'EDO.
# Chaque solveur prend en entrée :
#   - F      : fonction F(t, u) définie dans model.py
#   - u0     : vecteur d'état initial (numpy array)
#   - t0, tf : temps initial et final (en années)
#   - h      : pas de temps

import numpy as np

def euler_explicite(F, u0, t0, tf, h):
    """
    Méthode d'Euler explicite.

    Schéma : u_{n+1} = u_n + h * F(t_n, u_n)

    C'est la méthode la plus simple : on approxime la dérivée au point
    actuel et on avance d'un pas h. Rapide à coder, mais conditionnellement
    stable — sur un système raide comme le nôtre, h doit rester très petit
    pour éviter que la solution explose.
    """

    # Construction de la grille temporelle
    t_values = np.arange(t0, tf + h, h)
    n_steps  = len(t_values)
    n_vars   = len(u0)

    # Tableau de stockage : une ligne par pas de temps, une colonne par variable
    U = np.zeros((n_steps, n_vars))
    U[0] = u0

    for n in range(n_steps - 1):
        U[n+1] = U[n] + h * F(t_values[n], U[n])

    return t_values, U# solvers.py
# Solveurs numériques pour le système d'EDO.
# Chaque solveur prend en entrée :
#   - F      : fonction F(t, u) définie dans model.py
#   - u0     : vecteur d'état initial (numpy array)
#   - t0, tf : temps initial et final (en années)
#   - h      : pas de temps

import numpy as np

def euler_explicite(F, u0, t0, tf, h):
    """
    Méthode d'Euler explicite.

    Schéma : u_{n+1} = u_n + h * F(t_n, u_n)

    C'est la méthode la plus simple : on approxime la dérivée au point
    actuel et on avance d'un pas h. Rapide à coder, mais conditionnellement
    stable — sur un système raide comme le nôtre, h doit rester très petit
    pour éviter que la solution explose.
    """

    # Construction de la grille temporelle
    t_values = np.arange(t0, tf + h, h)
    n_steps  = len(t_values)
    n_vars   = len(u0)

    # Tableau de stockage : une ligne par pas de temps, une colonne par variable
    U = np.zeros((n_steps, n_vars))
    U[0] = u0

    for n in range(n_steps - 1):
        U[n+1] = U[n] + h * F(t_values[n], U[n])

    return t_values, U
