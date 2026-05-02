# Projet d'Analyse Numérique
 
**Équipe :** Evrard, Romain, Thibaud, Zouhair.

## Objectif du Projet
Modéliser et simuler l'évolution d'un écosystème à 5 populations (Végétation, Wapitis/Orignaux, Cerfs, Loups, Ours) en résolvant numériquement un système de 5 EDO non linéaires couplées.

## ⚠️⚠️⚠️⚠️ 
**Avant de taper la moindre ligne de code, lisez le PDF du sujet (`main.pdf`) en entier !**  
Pour la soutenance il est important que tout le monde comprenne l'ensemble du projet. La soutenance compte pour beaucoup dans la note...

---

## Architecture du projet
`ProjetAN/`
* `README.md` : Ce fichier de documentation.
* `Rapport.tex` : Rapport final LaTeX (chacun complète sa section).
* `main.pdf` : Sujet du projet.
* `photos_rapport/`
* `code/`
  * `params.py` : [ROMAIN] Tous les paramètres du modèle et conditions initiales.
  * `model.py` : [ROMAIN] Fonction F(t, u) contenant les 5 EDO du système.
  * `solvers.py` : [ROMAIN & THIBAUD] Solveurs numériques (Euler explicite, implicite, RK4, Crank-Nicolson).
  * `main.py` : [ZOUHAIR] Point d'entrée, exécution des simulations et génération des graphiques.
  

> **Important :** Chacun travaille dans son périmètre et ne réécrit pas le travail des autres. Ce README est a mettre à jour à chacune de nos contributions. 

---

## Répartition du Projet 

| Étape | Membre | Rôle & Tâches Principales | Livrables |
| :---: | :--- | :--- | :--- |
| **1** | **Evrard** |  Initialisation Git, coordination, README. | Introduction, Conclusion, Annexe. |
| **2** | **Romain** |  Architecture Python, EDO et paramètres. | Documentation du code et équations. |
| **3** | **Thibaud** |  Solveur d'Euler implicite et Newton-Raphson. | Justification des méthodes numériques. |
| **4** | **Zouhair** |  Scénario Yellowstone et graphiques. | Analyse des résultats et slides oraux. |

---

## Suivi du temps de travail (Validé)
* **Evrard :** 1h30
* **Romain :** 2h10
* **Thibaud :** 2h00
* **Zouhair :** 3h30
