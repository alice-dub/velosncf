export DATE=$(date '+%Y-%m-%d')
curl https://eu.ftp.opendatasoft.com/sncf/gtfs/export-ter-gtfs-last.zip --output historiques/$DATE-TER.zip
curl https://eu.ftp.opendatasoft.com/sncf/gtfs/export-intercites-gtfs-last.zip --output historiques/$DATE-intercite.zip
curl https://eu.ftp.opendatasoft.com/sncf/gtfs/transilien-gtfs.zip --output historiques/$DATE-transilien.zip
curl https://eu.ftp.opendatasoft.com/sncf/gtfs/export_gtfs_voyages.zip --output historiques/$DATE-transilien.zip
