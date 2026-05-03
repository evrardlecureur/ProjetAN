# Script de Soutenance — Cascade Trophique
## Projet Analyse Numérique 2025-2026 | 10 minutes | Evrard · Romain · Thibaud · Zhouair

---

> **Minutage indicatif** : 10 min = 600 sec  
> Chaque section indique l'intervenant et le temps cible.  
> Les **[crochets]** signalent les moments où changer de slide.

---

## SLIDE 1 — Titre (30 sec) — *Evrard*

*[SLIDE 1 — Titre]*

Bonjour à tous. Nous présentons notre projet d'Analyse Numérique sur la modélisation d'une cascade trophique.

Notre équipe : Evrard, Romain, Thibaud et Zhouair.

L'objectif : résoudre numériquement un système de cinq équations différentielles ordinaires non linéaires représentant l'évolution de cinq populations en interaction — végétation, wapitis, cerfs, loups et ours — et étudier l'impact d'une réintroduction de loups dans cet écosystème.

---

## SLIDE 2 — Contexte & Motivation (60 sec) — *Evrard*

*[SLIDE 2 — Contexte]*

Une cascade trophique, c'est l'idée qu'un prédateur ne régule pas seulement ses proies directes — son effet se propage à travers tout le réseau trophique, jusqu'à la végétation.

Des études de terrain de long terme — notamment à Isle Royale avec 41 ans de données loups-orignaux, et à Yellowstone depuis la réintroduction des loups en 1995 — ont révélé des dynamiques bien plus riches que les équations classiques de Lotka-Volterra.

En particulier, la prédation des loups suit une réponse **dépendante du ratio** — le taux de mise à mort dépend du rapport prédateurs/proies, pas seulement de la densité des proies. La régulation des ongulés suit un modèle **thêta-logistique** avec θ ≈ 4, plus brutal que le modèle logistique standard. Et la réponse numérique des loups est logarithmique.

Enfin, ce système est **raide** : il couvre des échelles allant du sub-annuel — le forçage saisonnier de la chasse — au décennal pour les ours et les loups. C'est précisément cette raideur qui justifie de comparer nos méthodes numériques.

---

## SLIDE 3 — Le Modèle Mathématique (90 sec) — *Romain*

*[SLIDE 3 — Modèle]*

Le vecteur d'état est à cinq composantes. Je vais vous présenter rapidement la structure des équations.

La **végétation V** suit une logistique standard, freinée par le pâturage des trois herbivores via des réponses de Holling type II — chaque terme a une demi-saturation différente, car les wapitis, cerfs et ours exploitent des strates de végétation différentes.

Les **ongulés** — wapitis N et cerfs D — suivent une croissance **thêta-logistique de Gilpin-Ayala**. La capacité de charge dépend de la végétation via une saturation de Monod : quand V tend vers zéro, κ tend vers zéro — c'est la famine. Les exposants θ_N = 4 et θ_D = 2 produisent une régulation bien plus abrupte qu'un modèle classique.

Les **loups W** ont un taux de croissance individuel logarithmique : r_W = ε₁·ln(Φ_W + η) − ε₂, directement tiré de Vucetich et al. 2011 calibré sur 41 ans de données. Le terme sin²(πt) crée le forçage saisonnier de la chasse, avec un pic tous les ans.

Les **ours B** sont omnivores : leur gain énergétique combine la prédation sur les ongulés et la consommation directe de végétation. C'est ce qui explique leur croissance monotone dans nos simulations — ils n'ont pas de prédateur supérieur.

---

## SLIDE 4 — Paramètres (30 sec) — *Romain*

*[SLIDE 4 — Paramètres]*

Tous les paramètres sont tirés directement du tableau page 7 du sujet — 23 constantes au total, regroupées par espèce dans `params.py`.

Les conditions initiales représentent l'état juste après une première réintroduction : végétation dense à 440, ongulés abondants, loups très peu nombreux à 0.04 animaux/km², ours modérés.

---

## SLIDE 5 — Méthodes Numériques (90 sec) — *Thibaud*

*[SLIDE 5 — Méthodes]*

Nous avons implémenté quatre méthodes numériques from scratch en Python pur.

**Euler explicite** : le schéma le plus simple, un pas vers l'avant. Conditionnellement stable. Sur ce système raide, un pas h = 0.5 an produit des erreurs de phase visibles sur les loups — environ 2.5% par oscillation saisonnière. Un pas h > 0.8 environ ferait diverger la solution.

**Euler implicite** : le schéma backward. A-stable — inconditionnellement stable. À chaque pas, on résout un système non linéaire par Newton-Raphson. Même avec h = 0.5, la trajectoire reste stable bien que l'erreur de phase soit de signe opposé à Euler explicite.

**Crank-Nicolson** : la règle du trapèze implicite. Ordre 2, A-stable, symétrique en temps. Avec le même h = 0.5, la précision est environ dix fois meilleure qu'Euler implicite — on se superpose pratiquement à la référence RK4.

**Runge-Kutta 4** : quatre évaluations de F par pas, ordre 4. Utilisé comme référence quasi-exacte à h = 0.005 an. L'erreur sur 10 ans est inférieure à 10⁻¹⁰.

---

## SLIDE 6 — Architecture Python (30 sec) — *Romain*

*[SLIDE 6 — Architecture]*

Le code est organisé en quatre modules : `params.py` concentre tous les paramètres, `model.py` implémente la fonction F(t,u) avec ses cinq équations, `solvers.py` contient les quatre solveurs et le Newton-Raphson vectoriel, et `main.py` orchestre les simulations et génère les cinq figures.

---

## SLIDE 7 — Simulation de référence (60 sec) — *Zhouair*

*[SLIDE 7 — Simulation de base]*

Voici la simulation de référence sur 50 ans avec RK4 à h = 0.005 an, soit environ 1.8 jour.

On observe plusieurs comportements intéressants. La **végétation** décroît rapidement les premières années, sous l'effet du pâturage intense, puis se stabilise aux alentours de 434 kg/km² avant de remonter très lentement.

Les **wapitis** croissent jusqu'à un pic vers 4.71 animaux/km² aux alentours de t = 25 ans, puis décroissent sous la pression combinée des loups et des ours.

Les **loups** montrent clairement les oscillations saisonnières annuelles du terme sin²(πt) — ces "dents de scie" correspondent aux saisons de chasse. Leur densité décline lentement car la ressource en proies diminue.

Les **ours**, omnivores sans prédateur supérieur, croissent de façon monotone jusqu'à environ 1 animal/km² à t = 50 ans.

---

## SLIDE 8 — Comparaison des solveurs (60 sec) — *Thibaud*

*[SLIDE 8 — Comparaison]*

Sur cette figure, on compare les quatre solveurs. RK4 à h = 0.005 est la référence. Les trois autres utilisent h = 0.5 an — seulement deux points par oscillation saisonnière d'un an.

Le résultat est frappant : pour la végétation, les wapitis, les cerfs et les ours, les quatre courbes sont pratiquement indiscernables à cette échelle. C'est là que les méthodes implicites montrent tout leur intérêt — à h égal à celui d'Euler explicite, elles donnent une précision bien supérieure.

La divergence est visible sur les **loups** : Euler explicite présente un léger décalage de phase positif, Euler implicite un décalage négatif. Crank-Nicolson reste collé à RK4. C'est une validation directe des ordres de convergence.

---

## SLIDE 9 — Convergence (60 sec) — *Thibaud*

*[SLIDE 9 — Convergence]*

Pour quantifier précisément les ordres de convergence, nous avons mesuré l'erreur relative en norme L² au temps final T = 10 ans, en faisant varier le pas de discrétisation entre h = 0.002 et h = 0.064.

Sur ce graphe log-log, la pente des droites donne l'ordre empirique. On retrouve bien les ordres théoriques : Euler explicite et implicite convergent en O(h) avec une pente ≈ 1. Crank-Nicolson converge en O(h²) — pente ≈ 3.6 légèrement supérieure au théorique car le système est lisse et les constantes d'erreur très favorables.

RK4 présente une pente apparente de 7.4 — supérieure au théorique de 4 — parce qu'aux petits pas, l'erreur atteint la **précision machine** (≈ 10⁻¹⁵). L'erreur d'arrondi domine alors, et la pente mesurée ne correspond plus à l'ordre de la méthode.

---

## SLIDE 10 — Scénario Yellowstone (60 sec) — *Zhouair*

*[SLIDE 10 — Yellowstone]*

Nous avons modélisé un scénario inspiré de la réintroduction historique des loups à Yellowstone en 1995.

Le protocole : pendant les 20 premières années, W = 0 exactement. Le terme dW/dt est proportionnel à W, donc zéro loups reste un équilibre stable. À t = 20 ans, on introduit W = 0.04 animaux/km² — les mêmes conditions initiales que la simulation de référence.

Pendant la **phase sans loups**, les wapitis prolifèrent jusqu'à 5.5 animaux/km² — soit 22% de plus que dans la référence. La végétation se dégrade, tombant à environ 424 kg/km². Les ours croissent librement.

À la **réintroduction**, on observe immédiatement la cascade trophique se mettre en place : la prédation augmente, les ongulés diminuent, le pâturage diminue, et la végétation commence à se régénérer — elle regagne environ 10 kg/km² par rapport à son creux.

---

## SLIDE 11 — Portraits de phase (30 sec) — *Zhouair*

*[SLIDE 11 — Portraits de phase]*

Les portraits de phase permettent de visualiser la trajectoire de l'écosystème dans l'espace des états.

Pour la simulation de référence, on voit une **spirale amortie** vers un attracteur dans le plan N-W — typique d'un système proie-prédateur à oscillations amorties.

Pour le scénario Yellowstone, le plan N-W montre clairement les 20 ans sans loups comme un point quasi-fixe à W = 0, puis la trajectoire qui remonte brutalement à la réintroduction.

---

## SLIDE 12 — Newton-Raphson (30 sec) — *Thibaud*

*[SLIDE 12 — Newton-Raphson]*

Le cœur des méthodes implicites est la résolution du système non linéaire G(u) = 0 à chaque pas. Nous avons implémenté un Newton-Raphson vectoriel avec un Jacobien approché par différences finies centrées, colonne par colonne. L'incrément ε est la racine carrée de l'epsilon machine, soit environ 1.49·10⁻⁸.

À chaque itération, on résout le système linéaire J·δ = −G(u) par élimination gaussienne via `np.linalg.solve`. La convergence est atteinte en 3 à 6 itérations en pratique, pour un coût d'environ 30 à 60 évaluations de F par pas — contre 4 pour RK4. C'est le prix de la stabilité inconditionnelle.

---

## SLIDE 13 — Conclusion (30 sec) — *Evrard*

*[SLIDE 13 — Conclusion]*

Pour conclure, ce projet nous a permis de mettre en œuvre un modèle biologique réaliste à cinq espèces, d'implémenter et de valider quatre solveurs numériques — dont deux méthodes implicites avec Newton-Raphson from scratch — de vérifier numériquement les ordres de convergence théoriques, et de simuler et interpréter un scénario de réintroduction de prédateur dans un écosystème.

Le résultat le plus marquant : sur ce système raide, Euler implicite et Crank-Nicolson permettent d'utiliser un pas 100 fois plus grand que RK4, tout en restant stables. La raideur justifie pleinement l'usage de schémas implicites.

Merci pour votre attention. Nous sommes prêts pour vos questions.

---

## Questions fréquentes — Réponses préparées

**Q : Pourquoi ne pas utiliser scipy.solve_ivp ?**
> Le sujet exige des implémentations from scratch. C'est l'objet même du cours d'analyse numérique — comprendre les mécanismes internes des solveurs, pas les utiliser comme boîte noire.

**Q : Pourquoi le pas de référence est-il h = 0.005 et non h = 0.001 ?**
> À h = 0.005, l'erreur de RK4 est déjà inférieure à 10⁻¹⁰ en norme relative sur 10 ans. Descendre à h = 0.001 multiplie le temps de calcul par 5 sans gain pratique. La vérification par la courbe de convergence fig5 confirme qu'à ce pas, l'erreur est dans le plancher numérique.

**Q : Le scénario Yellowstone est-il réaliste écologiquement ?**
> Les paramètres sont biologiquement plausibles (tirés de la littérature), mais le modèle est simplifié. En particulier, on néglige la structure d'âge, la dispersion spatiale, et les phénomènes comportementaux (ecology of fear). Néanmoins, les tendances qualitatives — augmentation de la végétation, diminution des wapitis après réintroduction — correspondent aux observations de terrain à Yellowstone.

**Q : Pourquoi l'ordre empirique de RK4 est-il 7.4 au lieu de 4 ?**
> Pour les petits pas h ≤ 0.002, l'erreur de troncature descend en dessous de la précision machine (≈ 10⁻¹⁵). On mesure alors l'erreur d'arrondi, qui se comporte différemment selon h. La pente mesurée en log-log ne correspond plus à l'ordre de la méthode mais au comportement de l'erreur numérique. C'est pour ça qu'on dit que RK4 a "atteint le plancher".

**Q : Pourquoi Crank-Nicolson donne p ≈ 3.6 au lieu de 2 ?**
> Les constantes d'erreur de Crank-Nicolson sont très favorables sur ce système (les dérivées d'ordre 3 sont petites dans la plage de h testée). En pratique, on est dans un régime pré-asymptotique où l'ordre apparent est supérieur à l'ordre asymptotique. Si on testait des h beaucoup plus petits, on convergerait vers 2.

**Q : Comment fonctionne exactement le forçage saisonnier ?**
> Le terme μ_W · sin²(πt) · W a une période T = 1 an. Il est nul en t = 0, 1, 2... (printemps-été) et maximal en t = 0.5, 1.5... (automne-hiver — la saison de chasse). Il représente la mortalité additionnelle due à la chasse humaine saisonnière. Les "dents de scie" visibles sur la courbe des loups dans fig1 correspondent exactement à ces pics annuels.

---

*Fin du script — Bonne soutenance !*
