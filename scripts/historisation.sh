export DATE=$(date '+%Y-%m-%d')

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

rm -r ../select-gare/public/data/gares_accessibles_carTER
rm -r ../select-gare/public/data/gares_accessibles_intercite
rm -r ../select-gare/public/data/gares_accessibles_TER
rm -r ../select-gare/public/data/gares_accessibles_TGV
rm -r ../select-gare/public/data/gares_accessibles_transilien

rm ../select-gare/src/components/liste_station.json
rm ../select-gare/src/components/periode_analyse.json

mv gares_accessibles_carTER ../select-gare/public/data/
mv gares_accessibles_intercite ../select-gare/public/data/
mv gares_accessibles_TER ../select-gare/public/data/
mv gares_accessibles_TGV ../select-gare/public/data/
mv gares_accessibles_transilien ../select-gare/public/data/

mv liste_station.json ../select-gare/src/components/
mv periode_analyse.json ../select-gare/src/components/
