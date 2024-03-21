source ../.env
echo "Using args:\n"
echo "\tCluster URI: ${MDBCONNSTR}\n"
mongorestore --uri="${MDBCONNSTR}" --authenticationDatabase=admin
echo ">>> Data loaded <<<"
echo
echo ">>> Creating search indexes <<<<"
mongosh "${MDBCONNSTR}" -f create-search-indexes.js
echo
echo "Done!"
