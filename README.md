# velosncf

Ce projet ? Visualiser faculement tous les trajets disponibles grâce à la SNCF ! (TGV, Intercité, TER, Car TER)

Une version est disponible en ligne sur https://trainvelo.succo.fr/

Ce projet s'appuie sur les GTFS téléchargeables depuis le portail opendata de la SNCF :  https://ressources.data.sncf.com/explore/?q=gtfs&sort=modified pour repérer tous les trajets proposés par la SNCF, et sur l' API de la BAN : https://adresse.data.gouv.fr/api-doc/adresse  permettant d'identifier les gares proches d'un lieu 
(fortement inspiré du site https://trainvelo.fr/ )

Le dossier **scripts** contient un script python permettant de créer les fichiers geojson utilisés par l'app à partir des données gtfs (fichiers à copier coller dans le dossier select-gare/public/data où l'app va ensuite les chercher. Le fichier liste_station.json, servant pour l'autocomplete et le calcul des distances lieu / gares est à mettre dans le dossier select-gare/src/components)

Le dossier **select-gare** contient l'application react js, à lancer en local avec la commande npm start.

TODO : 

* Le but initial du projet était de faciliter les trajets train avec vélo non démonté 🚲 (avec place réservable ou non). En effet cette recherche est compliquée car le site de la SNCF ne permet pas de faire un voyage combinant les places vélo réservables (intecité par ex.) et non (TER par ex.).
Je n'ai pas réussi à récupérer cette information (les GTFS de la SNCF n'intègrent pas, à mon grand désespoir, le champ *bikes_allowed*, et aucun champ GTFS ne semble prévu pour indiquer si le moyen de transport nécessite ou non une réservation). **Si vous avez des idées / indications pour m'aider sur ces sujets je suis très preneuse !**

* La carte permet d'identifier un trajet sympa : Permettre d'accéder aux horaires du train / car correspondant serait utile ! 
  ** En créant un lien directement vers la fiche horaire de SNCF connect de type https://www.sncf-connect.com/train/horaires/paris/abbeville. Problème : cette carte existe elle pour toutes les gares ? Comment formater le lien sncf-connect.com/train/horaires/%s/%s pour accéder à une page valide ? 
  ** En exploitant les données horaires présentes dans les GTFS : un autre chantier, qui nécessite surement de passer par une base de donnée ? 
  ** Autre piste : utiliser l'API navitia… quelle faisabilité ? 

* Elargir les données de la carte à d'autres opérateurs (Flixbus par exemple) ou sur une échelle plus importante (Europe)

* Harmoniser les noms des gares, qui n'est pas le même dans les différentes bases de la SNCF. Par exemple pour Bercy : 
![Screenshot](screenshot.jpeg)

* Permettre l'affichage d'indicateurs pertinents (durée min/max/moyenne du trajes, nombre de trajet par jour…)