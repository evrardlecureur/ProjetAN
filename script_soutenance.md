# Script de Soutenance — Cascade Trophique
## Projet Analyse Numérique 2025-2026 | Evrard · Romain · Thibaud · Zouhair
### Enseignants : C. Boulbe & V. Vadez — MAM, Polytech Nice Sophia

---

> **Conventions de lecture**
> - *[SLIDE N]* → changer de slide à ce moment
> - **Gras** → insister à l'oral, ralentir
> - *Italique* → commentaire de mise en scène, ne pas lire
> - Les réponses aux questions fréquentes sont en fin de document

---

## SLIDE 1 — Titre — *Evrard*

*[SLIDE 1 — Titre]*

Bonjour à tous. Aujourd'hui, Romain, Thibaud, Zouhair et moi-même allons vous présenter notre projet d'analyse numérique. On a travaillé sur la modélisation d'une cascade trophique.

Concrètement, on avait deux grands objectifs. Le premier, c'était de réussir à coder et à résoudre un système complexe de 5 équations différentielles. Ces équations, elles représentent 5 espèces qui interagissent : la végétation, les wapitis, les cerfs, les loups et les ours.

Notre deuxième objectif, c'était d'utiliser ce modèle mathématique pour simuler un événement écologique réel : la fameuse réintroduction des loups dans le parc de Yellowstone en 1995.

Pour vous expliquer tout ça, on va suivre le déroulé logique de notre travail : d'abord le contexte biologique, ensuite les maths, puis notre code, et enfin l'analyse de nos résultats.

---

## SLIDE 2 — Contexte & Motivation — *Evrard*

*[SLIDE 2 — Contexte]*

Pour commencer, c'est quoi une cascade trophique ? En fait, c'est l'idée qu'un super-prédateur, comme le loup, ne fait pas que manger ses proies. Son impact redescend « en cascade » sur tout le reste de l'écosystème, jusqu'à modifier la végétation.

On le sait grâce à des observations de très long terme sur le terrain. Et ces données nous ont prouvé que les équations de prédation classiques qu'on voit en cours, comme Lotka-Volterra, ne suffisaient pas pour la vraie vie.

Pour que notre modèle soit réaliste, on a dû y intégrer trois vrais comportements de terrain :

L'appétit des loups dépend du ratio entre le nombre de loups et de proies, pas juste du nombre de proies disponibles.

La croissance des herbivores suit un modèle thêta-logistique. C'est un grand mot pour dire que tant qu'il y a de la nourriture, ils se reproduisent très vite, mais dès qu'on atteint la limite du milieu, la régulation est brutale.

Chez les loups, la croissance est logarithmique : manger deux fois plus de wapitis ne veut pas dire qu'ils feront deux fois plus de petits. Le bénéfice finit par saturer.

Quand on met tout ça ensemble, on obtient un système mathématiquement très « raide ». Pourquoi ? Parce qu'on mélange des choses qui évoluent très vite, comme le cycle annuel des saisons, avec des choses très lentes, comme la démographie des ours qui prend des dizaines d'années.

C'est exactement cette différence d'échelles qui a rendu la résolution numérique difficile. Et Romain va justement vous présenter nos équations de plus près.

---

## SLIDE 3 — Le Modèle Mathématique — *Romain*

*[SLIDE 3 — Modèle]*

Le vecteur d'état de notre système contient cinq composantes : V pour la végétation, N pour les wapitis, D pour les cerfs, W pour les loups, et B pour les ours. On va voir la logique biologique derrière chaque équation.

**Végétation.** La végétation suit une croissance logistique standard vers une capacité de charge maximale de 500 kg par km². Elle est freinée par le pâturage des trois herbivores. Chaque terme de pâturage est une réponse de Holling Type II d'après l'énoncé, avec une demi-saturation différente pour chaque espèce, parce que wapitis, cerfs et ours n'exploitent pas les mêmes types de végétation.

**Wapitis et cerfs.** Ces deux populations suivent une croissance thêta-logistique de Gilpin-Ayala. On utilise θ = 4 pour les wapitis parce qu'avec θ = 1 ou 2, la régulation à la capacité de charge est trop douce — les ongulés la dépassent facilement. Avec θ = 4, la régulation devient très abrupte dès qu'on s'en approche, ce qui correspond aux observations de terrain. La capacité de charge effective dépend de la végétation disponible via une saturation de Monod : quand la végétation tend vers zéro, la capacité de charge tend vers zéro aussi. C'est le mécanisme de famine.

Pour la prédation des loups sur les wapitis, on n'utilise pas une réponse proie-dépendante classique. On utilise une réponse ratio-dépendante, où le taux de mise à mort dépend du ratio loups sur wapitis et non de la densité de wapitis seule. Ce choix est justifié par 41 ans de données à Isle Royale qui montrent que le comportement de chasse des loups change avec leur propre densité.

**Loups.** Le taux de croissance individuel des loups est logarithmique, directement tiré de Vucetich et al. 2011 et calibré sur ces 41 ans de données. La relation est concave : manger plus aide à se reproduire, mais avec des rendements décroissants. Le paramètre η évite la divergence du logarithme quand l'apport alimentaire tend vers zéro. Le terme sin²(πt) introduit la chasse saisonnière humaine : nul en hiver, maximal en automne. C'est ce qui rend le système non autonome et contribue à sa raideur.

**Ours.** Les ours sont omnivores. Leur taux de croissance combine la prédation sur les deux populations d'ongulés et la consommation directe de végétation. Contrairement aux loups, aucun prélèvement humain ne pèse sur eux dans notre modèle, ce qui explique leur croissance monotone dans nos simulations.

---

## SLIDE 4 — Paramètres & Conditions Initiales — *Romain*

*[SLIDE 4 — Paramètres]*

Tous les paramètres sont tirés directement du tableau page 7 du sujet — 23 constantes au total, regroupées par espèce dans `params.py`. Pas d'estimation, pas d'ajustement : les valeurs sont données et biologiquement plausibles d'après l'énoncé.

Les conditions initiales représentent l'état écologique juste après une première réintroduction des loups : végétation dense à 440 kg·km⁻², ongulés abondants, loups très peu nombreux à 0.04 animaux/km², ours modérés à 0.25. C'est le point de départ de toutes nos simulations.

---

## SLIDE 5 — Méthodes Numériques — *Thibaud*

*[SLIDE 5 — Méthodes]*

Nous avons implémenté quatre méthodes numériques **from scratch en Python pur** — sans scipy, sans odeint, sans boîte noire.

Avant de les présenter, un mot sur la raideur. Un système est raide quand son Jacobien a des valeurs propres de parties réelles de modules très différents. Ici, la végétation réagit en quelques mois, les loups en quelques années, les ours en une décennie — un rapport d'échelles d'environ 100. Euler explicite est contraint d'utiliser le pas le plus petit de toutes ces dynamiques pour rester stable — même quand on s'intéresse seulement aux ours. C'est le problème fondamental que les méthodes implicites résolvent.

**Euler explicite** : schéma forward, u_{n+1} = u_n + h·F(t_n, u_n). Un seul appel à F par pas, mais conditionnellement stable. Sur ce système, un pas h = 0.5 an produit des erreurs de phase visibles sur les loups — environ ±2.5% par oscillation saisonnière. Au-delà de h ≈ 0.8 an, la solution diverge.

**Euler implicite** : schéma backward, A-stable — inconditionnellement stable quelle que soit la valeur de h. À chaque pas, on résout le système non linéaire G(u_{n+1}) = 0 par Newton-Raphson. Même avec h = 0.5, la trajectoire reste stable, bien que l'erreur de phase soit de signe opposé à Euler explicite.

**Crank-Nicolson** : la règle du trapèze implicite, ordre 2, A-stable, symétrique en temps. Avec le même h = 0.5, la précision est environ dix fois meilleure qu'Euler implicite — la solution se superpose pratiquement à RK4. C'est la méthode la plus efficace sur ce système : même coût qu'Euler implicite, deux fois plus précise par ordre.

**Runge-Kutta 4** : quatre évaluations de F par pas, ordre 4, mais explicite. Conditionnellement stable — il faut h ≤ 0.005 an sur ce système pour que l'erreur soit négligeable. Utilisé comme référence quasi-exacte.

---

## SLIDE 6 — Architecture du Code Python — *Evrard*

*[SLIDE 6 — Architecture]*

Avant de passer aux résultats, je vous fais un point rapide sur la structure de notre code Python. En tant que chef de projet, j'ai tenu à ce qu'on ait une architecture vraiment propre, divisée en 4 fichiers distincts.

D'abord, params.py : c'est notre dictionnaire. Il contient toutes les constantes et nos valeurs de départ. Si on veut changer un paramètre pour tester autre chose, on le fait là et ça met tout à jour d'un coup.
Ensuite, model.py : c'est ici qu'on a codé notre système des 5 équations.
Puis, le fichier solvers.py : c'est notre moteur mathématique, avec nos quatre méthodes d'intégration et l'algorithme de Newton.
Et enfin, main.py : c'est le chef d'orchestre qui lance les calculs et génère nos graphiques.

Comme vous pouvez le voir sur le tableau, on a divisé le travail intelligemment pour que chacun ait son propre périmètre et qu'on ne se marche pas dessus lors de nos fusions sur Git.

Et justement, Romain va maintenant vous montrer ce que ce code a produit concrètement.
---

## SLIDE 7 — Simulation de Référence — *Romain*

*[SLIDE 7 — Simulation de base]*

Cette simulation de référence sur 50 ans avec RK4 à h = 0.005 an — soit environ 1.8 jour par pas — **valide le modèle** : tous les comportements qualitatifs attendus de l'énoncé sont présents.

La **végétation** décroît rapidement les premières années sous l'effet du pâturage intense, puis se stabilise aux alentours de 434 kg·km⁻² — soit 6 kg sous la capacité de charge maximale K_V = 500. Le pâturage permanent maintient un écart non nul avec K_V, ce qui est écologiquement cohérent.

Les **wapitis** croissent jusqu'à un pic de 4.72 animaux·km⁻² vers t ≈ 15-20 ans, puis déclinent sous la pression combinée des loups et des ours. La dynamique thêta-logistique produit un pic plus marqué et un déclin plus abrupt qu'un modèle logistique classique.

Les **cerfs**  croissent rapidement sur les premières années jusqu'à un pic de 3.15 animaux·km⁻² vers t ≈ 8 ans, puis se stabilisent autour de 3.04 en régime permanent. Leur dynamique est moins spectaculaire que celle des wapitis parce que la prédation des loups sur les cerfs est proportionnellement moins intense que sur les wapitis. Les loups concentrent l'essentiel de leur effort sur les wapitis 

Les **loups** montrent clairement les oscillations saisonnières annuelles du terme sin²(πt) — ces dents de scie correspondent exactement aux saisons de chasse. Leur densité décline lentement de 0.04 vers 0.028 sur 50 ans, car la ressource en proies diminue progressivement.

Les **ours**, omnivores sans prédateur supérieur et sans prélèvement humain, croissent de façon monotone de 0.25 jusqu'à environ 1 animal·km⁻² à t = 50 ans — un facteur quatre. C'est la conséquence directe de leur omnivorie : ils bénéficient à la fois des ongulés et de la végétation.

---

## SLIDE 8 — Comparaison des Solveurs — *Zouhair*

*[SLIDE 8 — Comparaison]*

*[Zouhair présente : c'est lui qui a généré ces figures, il les commente de première main.]*

Sur cette figure, RK4 à h = 0.005 est la référence en noir. Les trois autres méthodes utilisent toutes h = 0.5 an — seulement deux points par oscillation saisonnière de période T = 1 an.

Commençons par ce qui ne diverge pas. Pour la végétation, les wapitis, les cerfs et les ours — les quatre courbes sont pratiquement indiscernables. C'est là que les méthodes implicites montrent tout leur intérêt : avec un pas 100 fois plus grand que RK4, elles restent parfaitement stables et précises sur les dynamiques lentes.

La divergence est concentrée sur les **loups**, et c'est une validation directe des ordres de convergence. Euler explicite présente un décalage de phase positif d'environ +2.5% aux pics saisonniers — il anticipe le pic. Euler implicite présente un décalage de signe opposé, −2.4% — il retarde le pic. Ces erreurs de phase de sens contraire s'expliquent par la nature des schémas : l'un évalue F au début du pas, l'autre à la fin. **Crank-Nicolson fait la moyenne des deux — l'erreur se compense, et la courbe reste collée à RK4.**

Le zoom en bas de slide le montre très clairement : à h = 0.5 an, Euler explicite **divergerait** si on augmentait encore le pas. Euler implicite et Crank-Nicolson restent stables.

---

## SLIDE 9 — Analyse de Convergence — *Thibaud*

*[SLIDE 9 — Convergence]*

Pour quantifier les ordres de convergence, nous avons mesuré l'erreur relative en norme L² au temps final T = 10 ans en faisant varier le pas entre h = 0.002 et h = 0.064. La solution de référence est RK4 à h = 0.0005 an.

Sur ce graphe log-log, la pente des droites donne l'ordre empirique.

**Euler explicite et implicite** convergent en O(h) — pente ≈ 1, conforme au théorique.

**Crank-Nicolson** : pente mesurée ≈ 3.6, supérieure au théorique de 2. Pourquoi ? On est dans un régime pré-asymptotique : les dérivées d'ordre 3 de la solution sont petites dans cette plage de h, ce qui favorise Crank-Nicolson. Si on testait des h encore plus petits, on convergerait asymptotiquement vers la pente 2. La figure le montre d'ailleurs : sur les grands h, la pente effective approche 2.

**RK4** : pente apparente ≈ 7.4, bien supérieure au théorique de 4. C'est un artefact numérique. Pour les petits pas, l'erreur de troncature descend en dessous de la **précision machine** — environ 10⁻¹⁵. On mesure alors l'erreur d'arrondi, qui se comporte différemment. La pente ne correspond plus à l'ordre de la méthode, mais au plancher numérique. C'est une bonne chose : ça signifie que RK4 à h = 0.005 est essentiellement exact pour nos simulations.

---

## SLIDE 10 — Scénario Yellowstone — *Zouhair*

*[SLIDE 10 — Yellowstone]*

Nous avons modélisé un scénario inspiré de la réintroduction historique des loups à Yellowstone en 1995.

Le **protocole de simulation** repose sur une observation mathématique : dW/dt est proportionnel à W dans l'équation des loups. Donc si W(0) = 0, les loups restent absents — c'est un équilibre trivial stable. On peut donc simuler rigoureusement un écosystème sans loups simplement en posant W = 0 comme condition initiale. À t = 20 ans, on réintroduit W = 0.04 animaux·km⁻² et on reprend l'intégration à partir du dernier état de la phase sans loups.

**Phase sans loups, t = 0 à 20 ans.** Sans régulation par prédation, les wapitis prolifèrent librement jusqu'à **5.63 animaux·km⁻²**, soit **25% de plus** que dans la simulation de référence. Ce surnombre intensifie le pâturage : la végétation tombe à **422 kg·km⁻²**, son minimum sur toute la simulation. Les ours, eux, bénéficient de l'abondance d'ongulés et croissent plus vite qu'en référence.

**Réintroduction à t = 20 ans.** On observe immédiatement la cascade trophique se mettre en place. La prédation augmente, les ongulés diminuent, le pâturage diminue, la végétation commence à se régénérer.

**Phase post-réintroduction, t = 20 à 50 ans.** En régime quasi-permanent, comparé à la simulation de référence : la végétation est **+3 kg·km⁻²** plus dense, les wapitis sont **−0.28 animaux·km⁻²** moins nombreux, et les loups s'établissent légèrement plus haut à 0.035 — parce qu'ils ont trouvé un écosystème plus riche en proies.

Un point important : **le système ne revient pas à l'état initial**. Il garde la mémoire des 20 ans sans loups. Les wapitis restent en moyenne moins nombreux que dans la référence, la végétation reste légèrement plus dense — la cascade a eu lieu, mais à partir d'un état différent.

*[Point de comparaison qualitative à mentionner si on a le temps]* : À Yellowstone, entre 1995 et 2010, les biologistes ont observé une réduction significative des wapitis et un début de recolonisation végétale — notamment dans les zones riveraines. Notre modèle capture qualitativement ces tendances, même si les ordres de grandeur diffèrent d'un modèle simplifié à la réalité de terrain.

---

## SLIDE 11 — Portraits de Phase — *Zouhair*

*[SLIDE 11 — Portraits de phase]*

Les portraits de phase permettent de visualiser la **trajectoire de l'écosystème dans l'espace des états** — ce que le graphe temporel ne montre pas. La figure a quatre panneaux : deux pour la simulation de référence, deux pour le scénario Yellowstone.

**Référence N–W** : le plan N-W montre une spirale amortie vers un attracteur — typique d'un système proie-prédateur à oscillations amorties. Le système converge vers un point fixe stable vers t = 40 ans, il n'oscille pas indéfiniment. Le gradient de couleur du vert foncé vers le vert clair permet de suivre l'évolution temporelle — les premières années en bas à droite, le régime établi en haut à gauche.

**Référence D–W** : même comportement pour les cerfs, mais la spirale est plus rapide et plus petite. Les cerfs sont moins sensibles : le coefficient de prédation c_WD = 2.0 est bien plus faible que c_WN = 7.5, et θ_D = 2 produit une régulation moins brutale. La convergence est atteinte plus tôt.

**Yellowstone N–W** : pendant les 20 premières années, la trajectoire est presque horizontale à W ≈ 0 — les wapitis évoluent librement. À t = 20 ans, le saut vertical correspond à la réintroduction. La trajectoire remonte ensuite vers le même attracteur que la référence, mais via un transient beaucoup plus long, car le système repart d'un état très éloigné.

**Yellowstone D–W** : les cerfs croissent librement jusqu'à D ≈ 3.2, puis subissent une légère pression post-réintroduction. La convergence est rapide — les cerfs sont moins ciblés par les loups que les wapitis, et leur dynamique revient rapidement à l'attracteur.

Les deux simulations convergent vers le même attracteur, mais depuis des états très différents.

---

## SLIDE 12 — Newton-Raphson Vectoriel — *Thibaud*

*[SLIDE 12 — Newton-Raphson]*

Le cœur des méthodes implicites est la résolution à chaque pas du système non linéaire G(u_{n+1}) = 0.

L'algorithme comporte trois étapes. D'abord, un **prédicteur par Euler explicite** : u⁰ = u_n + h·F(t_n, u_n). C'est une approximation grossière de u_{n+1}, mais suffisante pour initialiser Newton. Ensuite, le **Jacobien par différences finies centrées**, colonne par colonne : J[:,j] ≈ [G(u+ε·e_j) − G(u−ε·e_j)] / (2ε), avec ε = √ε_machine ≈ 1.49·10⁻⁸. Enfin, l'**itération de Newton** : on résout J·δ = −G(u) par élimination gaussienne via `numpy.linalg.solve`, puis u ← u + δ, jusqu'à ce que ‖G(u)‖ < 10⁻¹⁰.

Pourquoi le Jacobien est-il numérique et non analytique ? On aurait pu le calculer analytiquement — les équations sont connues, les dérivées partielles existent. Mais les différences finies nous donnent la **généricité** : ce Newton-Raphson fonctionne pour n'importe quelle fonction F, sans réécrire le Jacobien si le modèle change. C'est un choix de conception, pas un raccourci.

La convergence est atteinte en **3 à 6 itérations** en pratique — ce qui peut sembler surprenant avec un prédicteur aussi grossier. C'est parce que le système est suffisamment régulier : le bassin d'attraction de la solution est large, et le prédicteur tombe toujours dedans.

Le coût par pas : environ 30 à 60 évaluations de F, contre 4 pour RK4. C'est le prix de la stabilité inconditionnelle. Mais ce prix est amorti sur le nombre de pas : Euler implicite à h = 0.5 avec 60 évaluations de F par pas sur 100 pas au total, contre RK4 à h = 0.005 avec 4 évaluations par pas sur 10 000 pas — le coût total est comparable, avec une stabilité garantie.

---

## SLIDE 13 — Conclusion — *Evrard*

*[SLIDE 13 — Conclusion]*
Pour conclure... Notre projet partait d'une vraie question d'écologie : que se passe-t-il quand on réintroduit un super-prédateur dans un milieu qui n'en a pas vu depuis 20 ans ?

Pour y répondre sans faire exploser notre code, on a compris qu'il nous fallait un modèle robuste, et surtout, les bonnes méthodes numériques. Mathématiquement, la vraie leçon qu'on en tire, c'est qu'utiliser Euler implicite ou Crank-Nicolson, ce n'est pas qu'un détail technique pour faire joli. Face à un système aussi « raide », c'est une obligation. Sans ces méthodes stables, le temps de calcul aurait été insoutenable.

Et sur le plan écologique, le modèle nous a confirmé une chose fascinante : réintroduire le loup, ça ne remet pas simplement les compteurs à zéro. La nature a une mémoire. Après 20 ans de prolifération des herbivores, l'écosystème est profondément abîmé. La cascade trophique que l'on déclenche est donc beaucoup plus abrupte que si le loup n'était jamais parti.

C'est exactement ce que nos mathématiques ont prédit, et c'est ce que les biologistes ont réellement pu observer sur le terrain à Yellowstone.

Merci pour votre attention. Nous sommes prêts pour vos questions.

---

---

## Réponses aux questions fréquentes

---

**Q : Pourquoi ne pas utiliser `scipy.solve_ivp` ?**

Le sujet exige des implémentations from scratch. C'est l'objet même du cours d'analyse numérique — comprendre les mécanismes internes des solveurs, pas les utiliser comme boîte noire. Utiliser `scipy.solve_ivp` reviendrait à résoudre un problème de cryptographie en important une bibliothèque RSA.

---

**Q : Pourquoi le Jacobien est-il approché par différences finies et non calculé analytiquement ?**

On aurait pu le calculer analytiquement — les dérivées partielles de F existent et sont finies. Mais les différences finies centrées nous donnent la généricité : le même Newton-Raphson fonctionne pour n'importe quelle F, sans réécrire le Jacobien si le modèle change. Sur un système à 5 espèces, le Jacobien analytique ferait 25 termes — certains assez longs. L'erreur de différences finies centrées est en O(ε²) avec ε = √ε_machine ≈ 10⁻⁸, ce qui donne une précision de l'ordre de 10⁻¹⁶ — largement suffisante pour la convergence Newton.

---

**Q : Pourquoi le pas de référence est h = 0.005 an et non h = 0.001 ?**

À h = 0.005, l'erreur relative de RK4 est déjà inférieure à 10⁻¹⁰ sur 10 ans — on est dans le plancher numérique. La courbe de convergence (fig5) le confirme : à ce pas, l'erreur d'arrondi domine la troncature. Descendre à h = 0.001 multiplierait le temps de calcul par 5 sans aucun gain pratique. C'est une décision guidée par l'analyse de convergence elle-même.

---

**Q : Le scénario Yellowstone est-il réaliste écologiquement ?**

Les paramètres sont biologiquement plausibles — tirés de la littérature sur Isle Royale et Yellowstone. Mais le modèle est simplifié par construction. On néglige la structure d'âge des populations, la dispersion spatiale, les phénomènes comportementaux comme l'ecologie de la peur — fear ecology — où les proies modifient leur comportement spatial même en présence de peu de prédateurs. On néglige aussi la saisonnalité de la reproduction. Néanmoins, les tendances qualitatives correspondent aux observations : réduction des ongulés, régénération végétale, augmentation des ours grizzlis après la réintroduction des loups à Yellowstone entre 1995 et 2010.

---

**Q : Pourquoi l'ordre empirique de RK4 est-il 7.4 au lieu de 4 ?**

Pour les petits pas h ≤ 0.002, l'erreur de troncature descend en dessous de la précision machine, environ 10⁻¹⁵. On mesure alors l'erreur d'arrondi flottant, qui dépend de h différemment selon les opérations. La pente log-log ne correspond plus à l'ordre de la méthode mais au comportement de l'erreur numérique dans ce régime. C'est ce qu'on appelle le plancher numérique. C'est en réalité une bonne nouvelle : ça confirme que RK4 à h = 0.005 est aussi précis que possible sur cette machine.

---

**Q : Pourquoi Crank-Nicolson donne p ≈ 3.6 au lieu de 2 ?**

L'ordre 2 est l'ordre asymptotique — celui qu'on observe quand h → 0. Sur notre plage de h, on est dans un régime pré-asymptotique où les termes d'ordre supérieur de l'erreur de troncature ne sont pas encore négligeables. Les dérivées d'ordre 3 et 4 de la solution sont petites sur ce système dans cette plage de h, ce qui fait que les termes suivants dans le développement de Taylor contribuent favorablement. Si on testait des h beaucoup plus petits — avant le plancher numérique — on convergerait asymptotiquement vers la pente 2.

---

**Q : Comment fonctionne exactement le forçage saisonnier ?**

Le terme μ_W · sin²(πt) · W a une période T = 1 an. Il est nul en t = 0, 1, 2... représentant le printemps-été, et maximal en t = 0.5, 1.5... représentant l'automne-hiver — la saison de chasse. Il représente la mortalité additionnelle due à la chasse humaine. Les dents de scie visibles sur la courbe des loups dans fig1 correspondent exactement à ces pics annuels. C'est ce terme qui rend le système non autonome et contribue à la raideur.

---

**Q : Qu'est-ce que ce projet vous a appris ?**

*[Chaque membre répond pour lui-même — réponses préparées ci-dessous.]*

**Evrard** : *"J'ai compris que la modélisation n'est pas neutre. Le choix de la réponse ratio-dépendante pour les loups versus une réponse proie-dépendante classique change qualitativement la dynamique, pas seulement quantitativement. Deux modèles d'apparence proche peuvent produire des comportements écologiquement très différents."*

**Romain** : *"Implémenter F(t,u) m'a forcé à lire les équations ligne par ligne. J'ai réalisé que le terme η dans le logarithme des loups n'est pas anodin — sans lui, quand Φ_W tend vers zéro, le taux de croissance des loups diverge vers moins l'infini, ce qui est biologiquement absurde. Chaque paramètre a une justification, même les plus petits."*

**Thibaud** : *"Ce qui m'a surpris c'est que Newton-Raphson converge en 3 à 6 itérations même avec un prédicteur aussi grossier qu'Euler explicite. Le système est suffisamment régulier pour que le bassin d'attraction de la solution soit très large. J'aurais pensé qu'il fallait un meilleur prédicteur."*

**Zouhair** : *"Le scénario Yellowstone m'a montré que la dynamique post-réintroduction dépend fortement de l'état du système au moment de la réintroduction. Si on introduit les loups quand les wapitis sont à leur maximum après 20 ans de prolifération, la cascade est plus violente que si on les introduit en régime stable. Le système a une mémoire, et cette mémoire compte."*

---

*Fin du script — Bonne soutenance !*
