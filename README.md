# velosncf

Le but de ce projet ? Une carte de France avec tous les trajets en train accessibles avec un vélo non démonté !

Une version est disponible en ligne sur https://trainvelo.succo.fr/

Ce projet s'appuie sur les GTFS téléchargeables depuis le portail opendata de la SNCF :  https://ressources.data.sncf.com/explore/?q=gtfs&sort=modified

Mais comment passer d'un GTFS à une carte lisible et pas trop surchargée ? 
Les traitements suivants ont été appliqués : 

* Pour chaque route, récupération des trajets associés : 
    * Pour les TERs on suppose que toutes les routes suivent le meme trajet (avec plus ou moins de stops) : on selectionne alors le trajet avec le plus d'arret comme "représentant de la route"
    * Pour les intercités et TGV cette méthode n'est pas applicable car supprime les différentes branches (par exemple le TGV de la route Bretagne se sépare à Rennes : un trajet dessert la bretagne Nord et l'autre la Bretagne Sud : on veut bien garder les deux trajets !). On sélectionne alors comme "représentants de la route" les trajets avec le plus d'arrets pour un meme couple (depart, arrivée)


* Pour chaque route, regroupement des sous-trajets associés :
  * Pour le TGV de la route Bretagne, on veut inclure le trajet "Paris - Rennes" dans un autre trajet, par exemple "Paris Quimper", puique le paris Quimper s'arrête aussi à Rennes

* Pour des routes différentes regroupent des trajets identiques et sous trajets:
  * Parfois 2 routes ont en fait des trajets identiques ou des sous trajets: par exemple le trajet Paris - Latour de Carole apparait à la fois dans la route "Paris Austerlitz - Lourdes" et dans la route "Paris-Toulouse-Cerbère/Latour de Carol/Rodez/Albi". On regroupe donc ces deux routes en une seule meme route contenant l'ensemble des arrets des deux trajets. 
  * Cette moulinette fonctionne par itération et tourne deux fois
 
* Calcul du tracé de des trajets agrégés : 
  * On a ici créé des sortes de "supers trajets" regroupant tous les arrêts des trajets ayant les mêmes points de départ ou d'arrivée ou bien des étant des sous trajets d'autres trajets. On doit alors reconstituer les tracés liant tous les arrêts. On part pour cela de l'hypothese suivante :  le train va toujours à la gare la plus proche de la gare où il est arrété.

TO DO:
* Le nettoyage des données est satisfaisant sur les JDD des TERs et des intercités mais pas sur les données qui ont très peu de routes avec des trajets très différents : il faudrait réduire la notion des sous trajets 
* Développer une fonctionnalité (où trouver l'information ?) permettant de déterminer si la ligne TGV accepte - ou pas- des vélos dépliés 
