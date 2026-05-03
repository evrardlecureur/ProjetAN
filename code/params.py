# params.py - paramètres du modèle (tableau p.7 du sujet)

# Végétation
r_V  = 1.20
K_V  = 500.0
a_N  = 15.0
nu_N = 200.0
a_D  = 8.0
nu_D = 100.0
a_B  = 3.0
nu_B = 120.0

# Wapitis / orignaux
r_N     = 0.30
K_N     = 7.0
V_star  = 70.0
theta_N = 4.0
c_WN    = 7.5
beta    = 0.5
c_BN    = 0.5
h_BN    = 3.0
delta_N = 0.05

# Cerfs
r_D        = 0.50
K_D        = 4.0
V_starstar = 50.0
theta_D    = 2.0
c_WD       = 2.0
h_WD       = 2.0
c_BD       = 0.3
h_BD       = 1.5
delta_D    = 0.08

# Loups
eps1  = 0.25
eps2  = 0.50
eta   = 0.01
m_W   = 0.15
mu_W  = 0.10

# Ours
e_B = 0.12
e_V = 0.02
m_B = 0.08

# Conditions initiales (page 6 du sujet)
# juste après réintroduction des loups : végétation dense, peu de loups
V0 = 440.0
N0 = 4.5
D0 = 2.5
W0 = 0.04
B0 = 0.25
