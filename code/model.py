# model.py
# Implémentation du système des 5 EDO (F1 à F5)
# u = [V, N, D, W, B]

import numpy as np
from params import *

def F(t, u):
    V, N, D, W, B = u

    # capacités de charge qui dépendent de la végétation dispo (formule Monod)
    kappa_N = K_N * V / (V_star + V)
    kappa_D = K_D * V / (V_starstar + V)

    # termes de prédation
    # loups sur wapitis
    f_WN = c_WN * N / (W + beta * N)
    # loups sur cerfs
    f_WD = c_WD * D / (h_WD + D)
    # ours sur les deux
    f_BN = c_BN * N / (h_BN + N)
    f_BD = c_BD * D / (h_BD + D)

    # taux total de mise à mort par loup (utilisé dans F4)
    Phi_W = f_WN + f_WD

    # F1 --> végétation : logistique + pâturage des 3 herbivores
    dV = (r_V * V * (1 - V / K_V)
          - a_N * V * N / (nu_N + V)
          - a_D * V * D / (nu_D + V)
          - a_B * V * B / (nu_B + V))

    # F2 --> wapitis : thêta-logistique (theta=4 => régulation forte près de kappa)
    dN = (r_N * N * (1 - (N / kappa_N) ** theta_N)
          - f_WN * W
          - f_BN * B
          - delta_N * N)

    # F3 --> cerfs : même structure que wapitis
    dD = (r_D * D * (1 - (D / kappa_D) ** theta_D)
          - f_WD * W
          - f_BD * B
          - delta_D * D)

    # F4 --> loups
    # réponse numérique log (Vucetich 2011) : plus on mange, moins ça aide à se reproduire
    # sin²(pi*t) : chasse saisonnière, pic tous les ans en automne (t=0.5, 1.5, ...)
    r_W = eps1 * np.log(Phi_W + eta) - eps2
    dW  = r_W * W - m_W * W - mu_W * (np.sin(np.pi * t) ** 2) * W

    # F5 - ours : omnivores, mangent ongulés ET végétation
    dB = (e_B * (f_BN + f_BD) + e_V * a_B * V / (nu_B + V) - m_B) * B

    return np.array([dV, dN, dD, dW, dB])
