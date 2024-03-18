source .env
echo "Using args:\n"
echo "\tCluster URI: ${MDBCONNSTR}\n"
mongodump --uri="${MDBCONNSTR}" --authenticationDatabase=admin --db=shif