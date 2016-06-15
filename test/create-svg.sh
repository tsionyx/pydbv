#!/usr/bin/env bash


DEMO_DIR=/tmp/demo
rm -rf ${DEMO_DIR} && mkdir ${DEMO_DIR}

declare -A SQLITE_SOURCES
SQLITE_SOURCES['north']="https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/northwindextended/Northwind.Sqlite3.sql"
SQLITE_SOURCES['chinook']="https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"


for i in "${!SQLITE_SOURCES[@]}"; do
	sql="${SQLITE_SOURCES[$i]}"
    echo -n "${i} - "
    # remove unicode and other marks from downloaded source
    # insert transaction mechanics
    cat <(echo "BEGIN TRANSACTION;"; curl -s ${sql} | sed '1s/^\xEF\xBB\xBF//' ; echo -e "\nEND TRANSACTION;") > ${DEMO_DIR}/${i}.sql
    # make the database
    sqlite3 ${DEMO_DIR}/${i}.db3 <${DEMO_DIR}/${i}.sql > /dev/null
    # and finally get the SVG out of it
    python pydbv/model.py sqlite:///${DEMO_DIR}/${i}.db3 | tee ${DEMO_DIR}/${i}.gv | dot -Kdot -Tsvg > ${DEMO_DIR}/${i}.svg

    echo file://${DEMO_DIR}/${i}.svg
done
