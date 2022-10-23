export DATE=$(date '+%Y-%m-%d')
export DOSSIER_APP="../select-gare/public/data"

rm -r historiques/$DATE
mkdir -p historiques/$DATE

curl https://eu.ftp.opendatasoft.com/sncf/gtfs/export-ter-gtfs-last.zip --output historiques/TER.zip
mkdir -p historiques/$DATE/TER
unzip historiques/TER.zip -d historiques/$DATE/TER

curl https://eu.ftp.opendatasoft.com/sncf/gtfs/export-intercites-gtfs-last.zip --output historiques/intercite.zip
mkdir -p historiques/$DATE/intercite
unzip historiques/intercite.zip -d historiques/$DATE/intercite

curl https://eu.ftp.opendatasoft.com/sncf/gtfs/transilien-gtfs.zip --output historiques/transilien.zip
mkdir -p historiques/$DATE/transilien
unzip historiques/transilien.zip -d historiques/$DATE/transilien

curl https://eu.ftp.opendatasoft.com/sncf/gtfs/export_gtfs_voyages.zip --output historiques/TGV.zip
mkdir -p historiques/$DATE/TGV
unzip historiques/TGV.zip -d historiques/$DATE/TGV

rm historiques/*.zip
mkdir -p gares_accessibles_carTER
mkdir -p gares_accessibles_intercite
mkdir -p gares_accessibles_TER
mkdir -p gares_accessibles_TGV
mkdir -p gares_accessibles_transilien

python3 generation_json.py $DATE

rm -r $DOSSIER_APP/gares_accessibles_carTER
rm -r $DOSSIER_APP/gares_accessibles_intercite
rm -r $DOSSIER_APP/gares_accessibles_TER
rm -r $DOSSIER_APP/gares_accessibles_TGV
rm -r $DOSSIER_APP/gares_accessibles_transilien

rm $DOSSIER_APP/liste_station.json
rm $DOSSIER_APP/periode_analyse.json

mv gares_accessibles_carTER $DOSSIER_APP/
mv gares_accessibles_intercite $DOSSIER_APP/
mv gares_accessibles_TER $DOSSIER_APP/
mv gares_accessibles_TGV $DOSSIER_APP/
mv gares_accessibles_transilien $DOSSIER_APP/

mv liste_station.json $DOSSIER_APP/
mv periode_analyse.json $DOSSIER_APP/
