# Tennis Master Data
# _User Guide :_ 
Description :

Tennis data for Goat Players and Ranking Players and data comparaison for the big Three (Roger Federer, Novak Djokovic, Rafael Nadal).

Installation :
```sh
$ git clone URL_DU_DEPOT
```

Required Packages :
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

You can install them by using the command :
```sh
$ python -m pip install -r requirements.txt
```

Démarrage :
To start the project you need to go at its root and use the command :
```sh
$ ./main.py
```

Utilisation :
The dashboard contains two different pages :
- Tennis Players Data
- The Big Three

To change page you just need to click on one of the two links at the top left of the screen.

On the 'Tennis Players Data' page there are :
- A player table with two differents mode (Ranking and Goat), and on which you can add values with the checkbox under the table and click on a name to see the profile of a player
- An histogram which show a specific stat that you can change by selecting a group stat and a stat
-   A graph which show the histogram stat chose  in function of another stat selected that you can change by selecting a group stat and a stat
-   A players map with mode ranking and goat and a stat that you can modify

On the 'The Big Three' page there are :
- A profile table of the three players
- A statistic table of the three players for which you can change the groupe of stat
- Three statistic table for head to head between two players selected among the big three
- A table with the Grand Slam' s result for the three players
- A graphic which shows the evolution of the total of tournament win for the three players. The type of the tournament can be modify.
- An histogram and a map for each of the three players on which you can modifiy the stat that is study

The histogram and graph data is filtred (3%) to avoid error value.

Architecture :


Copyright :
Je déclare sur l’honneur que le code fourni a été produit par moi/nous même, à l’exception des lignes ci dessous.

Sources :
All the data was find on the website : 
ultimatetennisstatistics.com/

# RAPPORT D'ANALYSE
A l'aide de ce dashboard nous pouvons tirer plusieurs conclusion :

Tout d'abord les histogrammes de la page 'Tennis Players Data' nous montre vers quels valeurs chaque stat tend.
Par exemple : le pourcentage d'Ace tend vers 5% , le temps d'un points tourne autour des 40 secondes, la vitesse moyenne du premier service tend vers 190 km/h.

Ensuite les graphiques de la même page nous permettent de faire le lien entre les différentes stats.
Par exemple : le pourcentage d'Ace est en lien avec la vitesse moyenne de premier service. Donc plus le joueur sert vite, plus il a de chance de faire un Ace.

La map elle nous permet par exemple de voir que la France est le pays avec le plus de joueurs dans le top 400 (40) devant les USA (33) mais que par exemple si l'on vise seulement le top 100 les USA passe devant avec 11 contre 12. Au niveau des goat players par contre la domination américaine est écrasante avec 120 joueurs dans le top 600 très loin devant ses dauphins l'Espagne et l'Australie qui en possèdent 48. Le pays avec le plus de Grand Chelem chez les goat est aussi de loin les USA avec ces 61 grand chelems.

Pour le big three on constate que nos trois joueurs sont très différents dans leur profile à part pour la taille qui est pour chacun d'environ 1 m 85. 
Au niveau des stats on peut par exemple voir que Federer domine ses deux compairs au service, tandis que les 2 autres paraissent supérieurs à lui au retour, ce qui équilibre un peu la balance. Ai niveau du pourcentage de points gagnés les 3 sont très serré. Federer prend moins de temps à finir un match de part son temps pris en moyenne par point. Par contre il va plus souvent au tie-break que les 2 autres.

Au niveau des confrontations direct on peut voir que Djokovic à un ratio de victoire supérieur dans ces 2 duels tandis que nadal domine aussi Federer. Ce qui est étonnant est que malgrès qu'il soit dominé par ses 2 adversaires Federer a gagné plus de points que Djokovic dans leurs duels et presque autant que Nadal. Les matchs contre Nadal sont les plus longs et aussi les plus fréquents. On peut voir aussi que nadal surdomine ses adversaires sur terre battue mais sur les autres surfaces c'est lui qui est dominé.

An niveau des résultats en Grand Chelem on peut voir que les 3 sont très performant la plupart du temps. On voit notamment une domination écrasante de Federer de 2004 à 2009, ou de Nadal sur Rolland Garros depuis le début de sa carrière. Au niveau de la course au titre pour les Grand chelem d'abord on voit que Federer est resté loin devant jusqu'à 2009 avant de se faire rattraper au fur et à mesures par ses compairs qui l'égalisent tous les deux en 2021 avant de le doubler en 2022. Pour les titres en général Federer risque peu de se faire rattraper, mais Djokovic pourrait rattraper Nadal dans les prochaines années. Pour les masters 1000 Federer s'est vite fait distancer par Nadal et Djokovic qui se tiennent à la gorge

Pour les maps on voit que Nadal a du mal contre les russes contrairement aux 2 autres. En tout cas on voit bien que ces 3 joueurs domine pratiquement tous les pays. On voit aussi que les 3 ont majoritairement joués contre des français et des espagnols.

Pour les histogrames on voit que les 3 sont vraiment pratiquement identiques pour le pourcentage de point gagnés par match. Federer domine largement sur le nombre d'Ace par set. Dans la plupart des stats les 3 sont vraiment très serrés et cela montre à quel point ce sont des champions incontestés du tennis qui sont très dur à départager.

# Developer Guide
Le code peut-être modifier bien évidemment. Par exemple la création de la page du big three se fait à partir d'une liste avec leur 3 noms et de la data de leurs matches. On aurait juste à créer la data d'un autre joueur et d'ajouter sa liste au nom pour que la comparaison se fasse avec d'autres.

Architecture :






