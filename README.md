# Tennis Master Data
# _User Guide :_ 
Description :
Ce programme permet de récupérer de la data des joueurs de tennis et de l'afficher ensuite sur des graphiques, des tableaux, et des cartes. Les joueurs sont classé en tant que 'goat' (meilleurs joueurs de tous les temps) et 'ranking' (meilleurs joueurs actuels). Ce principe est très important dans la première page du dashboard. (Attention des joeurs peuvent être présents dans les 2 différents rangs).
Une analyse complète du Big Three (Roger Federer, Rafael Nadal, Novak Djokovic) est aussi effectuée, où leurs stats sont comparées sur tous les points par rapport à tout leurs matches.

Installation :
```sh
$ git clone https://github.com/lemagnyt/python-project
```

Packages requis :
| Package | Version |
| ------ | ------ |
| beautifulsoup4 | 4.11.1 |
| tqdm | 4.64.1 |
| requests | 2.28.1 |
| geopandas | 0.12.1 |
| pycountry | 22.3.5 |
| plotly-express | 0.4.1 |
| dash | 2.7.0 |
| dash-bootstrap-components | 1.2.1 |
| pandas | 1.5.1 |

Vous pouvez les installer en utilisant la commande :
```sh
$ python -m pip install -r requirements.txt
```

Démarrage :
Pour lancer le programme, utilisez la commande :
```sh
$ ./main.py
```

Utilisation :
Le dashboard contient deux différentes pages :
- Tennis Players Data
- The Big Three

Pour changer de page vous devez cliquer sur un des deux liens en haut à gauche de l'écran.

Sur la page 'Tennis Players Data' vous avez à votre disposition :
- Un tableau des joueurs suivi d'un tableau de profiles à sa droite. Vous pouvez changer entre les mode 'goat' et 'ranking' expliqués plus haut. En dessous du tableau vous avez des check box qui vous permettent d'afficher des infos supplémentaires dans le tableau. Enfin si vous cliquez sur un nom de joueur son profile s'affichera sur le tableau à droite. Vous pouvez d'ailleurs changer de page du tableau en cliquant sur les flèches en bas de celui-ci afin de voir les différents joueurs.
- Un histogramme révélant une statistique de tennis pour tous les joueurs présents dans la data. Avec le premier dropdown vous pouvez sélectionner le groupe de stats, puis avec le second vous pouvez choisir la stat voulu.
-  Un graphique qui montre le rapport entre deux différentes stats au tennis. La première stat est celle sélectionné pour l'histogramme, et la deuxième celle sélectionné au dessus du graphique avec le même principe que pour l'histogramme
- Une carte du monde affichant une stat par rapport à tous les joueurs de tennis du mode choisit. Le dropdown à gauche permet de choisir le mode (Ranking ou goat) et celui à droite permettant de choisir la stat qu'on veut afficher. Une hover-data bien précise est affiché selon la stat.

Sur la page 'Tennis Players Data' vous avez à votre disposition :
- Un tableau des profiles des 3 joueurs du Big Three
- Un tableau de statistiques dont on peut modifier le groupe de stat à l'aide d'un dropdown
- Trois tableaux permettant d'afficher les face à face entre 2 joueurs parmis les 3 que l'on choisit à l'aide des 2 dropdown
- Un tableau des résultat en grand chelem de nos 3 joueurs durant ses dernières années avec des couleurs pour les différentes surfaces (dur, terre et gazon) et des couleurs selon le résultat obtenu.
- Un graphique montrant l'évolution du nombre de tournois gagnés au fil des années. n peut changer le type de tournoi avec le dropdown et si on met la souris sur le graphique on peut comparer nos 3 joueurs pour une année.
- Un histogramme et une carte du monde pour les 3 joueurs, les 2 ayant une stat différente à montre que l'on peut changer avec les dropdown.

La data des histogrammes et graphiques a &té filtré à 3 % afin d'éviter les erreurs du site dans lesquels la data a été récupérée.

Architecture :


Copyright :
Je déclare sur l’honneur que le code fourni a été produit par moi/nous même, à l’exception des lignes ci dessous.

Sources :
All the data was find on the website : 
[Ultimate Tennis](ultimatetennisstatistics.com/)

# RAPPORT D'ANALYSE
A l'aide de ce dashboard nous pouvons tirer plusieurs conclusions :

Tout d'abord les histogrammes de la page 'Tennis Players Data' nous montre vers quels valeurs chaque stat tend.
Par exemple : le pourcentage d'Ace tend vers 5% , le temps d’un point tourne autour des 40 secondes, la vitesse moyenne du premier service tend vers 190 km/h.

Ensuite les graphiques de la même page nous permettent de faire le lien entre les différentes stats.
Par exemple : le pourcentage d'Ace est en lien avec la vitesse moyenne de premier service. Donc plus le joueur sert vite, plus il a de chance de faire un Ace.

La map elle nous permet par exemple de voir que la France est le pays avec le plus de joueurs dans le top 400 (40) devant les USA (33) mais que par exemple si l'on vise seulement le top 100 les USA passe devant avec 11 contre 12. Au niveau des joueurs ‘goat’ cependant la domination américaine est écrasante avec 120 joueurs dans le top 600 très loin devant ses dauphins l'Espagne et l'Australie qui en possèdent 48. Le pays avec le plus de Grand Chelem chez les ‘goat’ est aussi de loin les USA avec ces 61 grands chelems.

Pour le big three on constate que nos trois joueurs sont très différents dans leur profile à part pour la taille qui est pour chacun d'environ 1 m 85. 
Au niveau des stats on peut par exemple voir que Federer domine ses deux compairs au service, tandis que les 2 autres paraissent supérieurs à lui au retour, ce qui équilibre un peu la balance. Ai niveau du pourcentage de points gagnés les 3 sont très serré. Federer prend moins de temps à finir un match par son temps pris en moyenne par point. Cependant il va plus souvent au tie-break que les 2 autres.

Au niveau des confrontations direct on peut voir que Djokovic à un ratio de victoire supérieur dans ces 2 duels tandis que Nadal domine aussi Federer. Ce qui est étonnant est que malgré qu'il soit dominé par ses 2 adversaires Federer a gagné plus de points que Djokovic dans leurs duels et presque autant que Nadal. Les matchs contre Nadal sont les plus longs et aussi les plus fréquents. On peut voir aussi que Nadal surdomine ses adversaires sur terre battue mais sur les autres surfaces c'est lui qui est dominé.

An niveau des résultats en Grand Chelem on peut voir que les 3 sont très performant la plupart du temps. On voit notamment une domination écrasante de Federer de 2004 à 2009, ou de Nadal sur Rolland Garros depuis le début de sa carrière. Au niveau de la course au titre pour les Grand chelem d'abord on voit que Federer est resté loin devant jusqu'à 2009 avant de se faire rattraper au fur et à mesures par ses compairs qui l'égalisent tous les deux en 2021 avant de le doubler en 2022. Pour les titres en général Federer risque peu de se faire rattraper, mais Djokovic pourrait rattraper Nadal dans les prochaines années. Pour les masters 1000 Federer s'est vite fait distancer par Nadal et Djokovic qui se tiennent à la gorge

Pour les maps on voit que Nadal a du mal contre les Russes contrairement aux 2 autres. En tout cas on voit bien que ces 3 joueurs dominent pratiquement tous les pays. On voit aussi que les 3 ont majoritairement joués contre des Français et des Espagnols.

Pour les histogrammes on voit que les 3 sont vraiment pratiquement identiques pour le pourcentage de point gagnés par match. Federer domine largement sur le nombre d'Ace par set. Dans la plupart des stats les 3 sont vraiment très serrés et cela montre à quel point ce sont des champions incontestés du tennis qui sont très dur à départager.

En conclusion, ce dashboard nous permet de relever beaucoup de faits importants sur le tennis, nottamment sur la détermination du meilleur joueur de tous les temps qui paraît tellement compliquée tant les 3 joueurs se tiennent au coude à coude.

# Developer Guide
Le code peut être modifié bien évidemment. Par exemple la création de la page du big three se fait à partir d'une liste avec leur 3 noms et de la data de leurs matches. On aurait juste à créer la data d'un autre joueur et d'ajouter sa liste au nom pour que la comparaison se fasse avec d'autres. Pour n'importe quel joueur dont on a l'idée on peut donc récupérer toutes les infos sur chacun de ces matchs. D'autres stats peuvent être étudier parmi celle dont on a décidé de faire impasse. De nouveaux graphiques peuvent être réalisés et bien plus encore. La liste des choses possibles à faire est en effet très diversifiée au vu du nombre de statistiques que le tennis présente.

Important ! : Pour le programme main vous pouvez choisir ou non si le mode scraping est activé ou si vous voulez utiliser la data déjà présente en mettant dans les paramètre de la fonction create_dashboard, "mode_scraping = True". Cela télécharger la data de tous les joueurs et la data des matchs pour les 3 joueurs du big three. Sans le mode_sleep le processus devrait prendre 10 à 15 minutes. 

Vous pouvez tester les 2 principales fonction de scraping 'all_data_scraping' et 'matchesData' en ajoutant aux paramètres de la fonction 'test=True' afin de ne pas mélanger les datas. Les fichier json seront alors écrit avec un '_test' à la fin de leur nom.

Architecture : Le programme possède un fichier main.py permettant de lancer le programme, mais aussi un dossier modules où se trouve les différents codes permettant de scraper les données et de créer le dashboard. Le module 'TennisScraping' s'occupe de tout ce qui est data des joueurs ou des matchs à récupérer et mettre dans des fichiers, puis le module 'world-data.py' l'épaule en s'occupant de classer la data par pays et d'en faire une nouvelle data pour créer des cartes du monde. Le module 'app.py' lui va créer le dashboard multi-pages à l'aide du dossier Pages où se truve les deux différents codes pour les deux différentes pages du dashboard. Enfin dans assets nous retrouvons les différentes images et polices utiliser pour notre dashboard.
