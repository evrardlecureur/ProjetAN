# Projet d'Analyse Numérique : Étude d'une Cascade Trophique

Bienvenue sur le dépôt de notre projet d'Analyse Numérique (2025-2026).  
**Équipe :** Evrard, Romain, Thibaud, et Zhouair.

## Objectif du Projet

Modéliser et simuler l'évolution d'un écosystème à 5 populations (Végétation,
Wapitis/Orignaux, Cerfs, Loups, Ours) en résolvant numériquement un système de
5 EDO non linéaires couplées.

## 🚨 AVERTISSEMENT IMPORTANT POUR TOUTE L'ÉQUIPE 🚨

**Avant de taper la moindre ligne de code, lisez le PDF du sujet (`main.pdf`) en entier !**  
Les professeurs exigent que chaque membre maîtrise l'ensemble des notions mathématiques
et écologiques. La soutenance orale de 10 minutes est obligatoire — le temps de parole
sera réparti entre nous 4. Une absence ou un membre qui ne maîtrise pas le sujet peut
entraîner un 0 pour tout le groupe.

---

## Architecture du projet

ProjetAN/
├── README.md
├── Rapport.tex    ← rapport final (chacun complète sa section)
├── main.pdf       ← sujet du projet
└── code/
    ├── params.py     ← [ROMAIN] tous les paramètres du modèle (tableau p.7 du sujet)
    ├── model.py      ← [ROMAIN] fonction F(t, u) : les 5 EDO du système
    ├── solvers.py    ← [ROMAIN] Euler explicite  |  [THIBAUD] Euler implicite + autres
    └── main.py       ← [ROMAIN] point d'entrée   |  [ZHOUAIR] simulations & graphiques

> **Règle d'or :** chacun travaille dans son périmètre et ne réécrit pas le travail des autres.

---

## Répartition des Tâches

| Étape | Membre | Rôle & Tâches | Livrable rapport |
|-------|--------|---------------|-----------------|
| **1** | **Evrard** | Chef de projet, init Git, coordination | Introduction, Conclusion, Annexe |
| **2** | **Romain** | Architecture Python complète : `params.py`, `model.py`, Euler explicite dans `solvers.py`, `main.py` | Section "Modélisation mathématique" dans le rapport |
| **3** | **Thibaud** | Euler implicite + méthodes supplémentaires dans `solvers.py` | Section "Méthodes numériques et justification" |
| **4** | **Zhouair** | Simulations, graphiques, scénario Yellowstone via `main.py` | Section "Résultats et analyse" + slides soutenance |

---

## Contribution et communication

Ce README est un outil de travail collectif. **N'importe qui peut et doit le mettre à jour**
pour informer le groupe : avancement, blocage, changement dans la structure des fichiers,
décision prise, etc. C'est notre principal canal d'info entre les étapes.

De la même façon, **chacun documente sa partie dans `Rapport.tex`** au fur et à mesure —
ne pas tout laisser pour la fin.

---

## Suivi du temps de travail

*(À remplir au fur et à mesure — obligatoire pour l'annexe du rapport)*

- **Evrard :** 1h30
- **Romain :** en cours...
- **Thibaud :** en cours...
- **Zhouair :** en cours...
