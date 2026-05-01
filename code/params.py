# params.py
# Tous les paramètres du modèle, tirés directement du tableau page 7 du sujet.
# Unités et descriptions conservées en commentaire pour la lisibilité.

# --- Végétation (F1) ---
r_V  = 1.20   # an⁻¹       Taux de croissance intrinsèque de la végétation
K_V  = 500.0  # kg.km⁻²    Capacité de charge de la végétation
a_N  = 15.0   # kg.an⁻¹.animal⁻¹  Intensité de pâturage des wapitis/orignaux
nu_N = 200.0  # kg.km⁻²    Demi-saturation, pâturage wapitis sur V
a_D  = 8.0    # kg.an⁻¹.animal⁻¹  Intensité de pâturage des cerfs
nu_D = 100.0  # kg.km⁻²    Demi-saturation, pâturage cerfs sur V
a_B  = 3.0    # kg.an⁻¹.animal⁻¹  Intensité de pâturage des ours sur V
nu_B = 120.0  # kg.km⁻²    Demi-saturation, pâturage ours sur V

# --- Ongulés principaux : wapitis/orignaux (F2) ---
r_N  = 0.30   # an⁻¹       Taux de croissance intrinsèque
K_N  = 7.0    # animaux.km⁻²  Capacité de charge maximale
V_star = 70.0 # kg.km⁻²    Demi-saturation pour κ_N(V)
theta_N = 4.0 #  —          Exposant thêta-logistique
c_WN = 7.5    # km².animal⁻¹.an⁻¹  Coeff. mise à mort loup–wapiti
beta = 0.5    #  —          Paramètre de dépendance au ratio
c_BN = 0.5    # km².animal⁻¹.an⁻¹  Coeff. mise à mort ours–wapiti
h_BN = 3.0    # animaux.km⁻²  Demi-saturation ours–wapiti
delta_N = 0.05 # an⁻¹      Mortalité de fond des wapitis

# --- Ongulés secondaires : cerfs (F3) ---
r_D  = 0.50   # an⁻¹       Taux de croissance intrinsèque
K_D  = 4.0    # animaux.km⁻²  Capacité de charge maximale des cerfs
V_starstar = 50.0 # kg.km⁻²  Demi-saturation pour κ_D(V)
theta_D = 2.0 #  —          Exposant thêta-logistique
c_WD = 2.0    # km².animal⁻¹.an⁻¹  Coeff. mise à mort loups–cerfs
h_WD = 2.0    # animaux.km⁻²  Demi-saturation loups–cerfs
c_BD = 0.3    # km².animal⁻¹.an⁻¹  Coeff. mise à mort ours–cerfs
h_BD = 1.5    # animaux.km⁻²  Demi-saturation ours–cerfs
delta_D = 0.08 # an⁻¹      Mortalité de fond des cerfs

# --- Loups (F4) ---
eps1  = 0.25  #  —          Pente logarithmique de la réponse numérique
eps2  = 0.50  #  —          Décalage de base de la réponse numérique
eta   = 0.01  # an⁻¹        Décalage de régularisation logarithmique
m_W   = 0.15  # an⁻¹        Mortalité naturelle des loups
mu_W  = 0.10  # an⁻¹        Amplitude max du prélèvement saisonnier humain

# --- Ours (F5) ---
e_B  = 0.12   #  —          Gain énergétique des ours à partir des proies
e_V  = 0.02   # an⁻¹        Gain énergétique des ours à partir de la végétation
m_B  = 0.08   # an⁻¹        Mortalité naturelle des ours

# --- Conditions initiales (page 6 du sujet) ---
V0 = 440.0   # kg.km⁻²
N0 = 4.5     # animaux.km⁻²
D0 = 2.5     # animaux.km⁻²
W0 = 0.04    # animaux.km⁻²
B0 = 0.25    # animaux.km⁻²
