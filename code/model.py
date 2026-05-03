# model.py
# Fonction F(t, u) définissant le membre de droite des EDOs.
# u = [V, N, D, W, B]
# Retourne le vecteur dérivée [dV/dt, dN/dt, dD/dt, dW/dt, dB/dt]

import numpy as np
from params import *

def F(t, u):
    V, N, D, W, B = u

    # ------------------------------------------------------------------ #
    # Termes intermédiaires (utilisés dans plusieures EDOs)
    # ------------------------------------------------------------------ #

    # Capacités de charge dépendantes de la végétation (formule 6)
    kappa_N = K_N * V / (V_star    + V)   # pour wapitis
    kappa_D = K_D * V / (V_starstar + V)  # pour cerfs

    # Prédation des loups sur les wapitis (formule 2)
    f_WN = c_WN * N / (W + beta * N)

    # Prédation des loups sur les cerfs (formule 3)
    f_WD = c_WD * D / (h_WD + D)

    # Prédation des ours sur les wapitis et cerfs (formule 4)
    f_BN = c_BN * N / (h_BN + N)
    f_BD = c_BD * D / (h_BD + D)

    # Taux total de mise à mort par loup (formule 5)
    Phi_W = f_WN + f_WD

    # ------------------------------------------------------------------ #
    # F1 : Végétation
    # ------------------------------------------------------------------ #
    
    # Croissance logistique, freinée par le pâturage des 3 herbivores.
    # Chaque terme de pâturage est une réponse de Holling Type II sur V.
    dV = (r_V * V * (1 - V / K_V)
          - a_N * V * N / (nu_N + V)
          - a_D * V * D / (nu_D + V)
          - a_B * V * B / (nu_B + V))

    # ------------------------------------------------------------------ #
    # F2 : Ongulés principaux (wapitis/orignaux)
    # ------------------------------------------------------------------ #
    # Croissance thêta-logistique (Gilpin-Ayala) : avec theta_N=4, la régulation
    # par la capacité de charge est bien plus brutale qu'un modèle logistique classique.
    dN = (r_N * N * (1 - (N / kappa_N) ** theta_N)
          - f_WN * W
          - f_BN * B
          - delta_N * N)

    # ------------------------------------------------------------------ #
    # F3 : Ongulés secondaires (cerfs)
    # ------------------------------------------------------------------ #
    
    dD = (r_D * D * (1 - (D / kappa_D) ** theta_D)
          - f_WD * W
          - f_BD * B
          - delta_D * D)

    # ------------------------------------------------------------------ #
    # F4 : Loups
    # ------------------------------------------------------------------ #
    
    # Réponse numérique logarithmique (Vucetich et al. 2011) :
    # le taux de croissance individuel est concave; manger plus apporte
    # de moins en moins de bénéfice reproductif. eta évite log(0).
    # sin²(πt) crée un forçage saisonnier annuel (pic à t=0.5, 1.5, ... = automne).
    r_W = eps1 * np.log(Phi_W + eta) - eps2
    dW  = r_W * W - m_W * W - mu_W * np.sin(np.pi * t)**2 * W

    # ------------------------------------------------------------------ #
    # F5 : Ours
    # ------------------------------------------------------------------ #
    
    # Les ours sont omnivores : ils tirent de l'énergie des proies (f_BN, f_BD)
    # ET de la végétation directement (baies, racines...).
    dB = (e_B * (f_BN + f_BD) + e_V * a_B * V / (nu_B + V) - m_B) * B

    return np.array([dV, dN, dD, dW, dB])
