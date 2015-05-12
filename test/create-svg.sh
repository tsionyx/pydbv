#!/usr/bin/env bash
DEMO_DIR=/tmp/demo
rm -rf $DEMO_DIR && mkdir $DEMO_DIR
i=1
# run from root directory of the project
for sql in $(find downloads/*.sql); do
    echo $i.$sql
    sqlite3 $DEMO_DIR/$i.db3 < <(echo "BEGIN TRANSACTION;"; cat $sql ; echo "END TRANSACTION;")> /dev/null
    python pydbv/model.py sqlite:///$DEMO_DIR/$i.db3 | tee $DEMO_DIR/$i.gv | dot -Kdot -Tsvg > $DEMO_DIR/$i.svg
    ((i++))
done
