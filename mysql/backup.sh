#!/bin/bash
[ -z "${MYSQL_USER}" ] && { echo "=> MYSQL_USER cannot be empty" && exit 1; }
[ -z "${MYSQL_PASS:=$MYSQL_PASSWORD}" ] && { echo "=> MYSQL_PASS cannot be empty" && exit 1; }

DATE=$(date +%Y%m%d%H%M)
echo "=> Backup started at $DATE"
databases=${MYSQL_DATABASE:-${MYSQL_DB:-$(mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASS" -e "SHOW DATABASES;" | tr -d "| " | grep -v Database)}}
for db in $databases
do
  if [[ "$db" != "information_schema" ]] && [[ "$db" != "performance_schema" ]] && [[ "$db" != "mysql" ]] && [[ "$db" != _* ]]
  then
    echo "Dumping database: $db"
    FILENAME=/backup/$db.sql
    if mysqldump -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASS" --databases "$db" $MYSQLDUMP_OPTS > "$FILENAME"
    then
      gzip -f "$FILENAME"
    else
      rm -rf "$FILENAME"
    fi
  fi
done

if [ -n "$MAX_BACKUPS" ]
then
  while [ "$(find /backup -maxdepth 1 -name "*.sql.gz" | wc -l)" -gt "$MAX_BACKUPS" ]
  do
    TARGET=$(find /backup -maxdepth 1 -name "*.sql.gz" | sort | head -n 1)
    echo "Backup $TARGET is deleted"
    rm -rf "$TARGET"
  done
fi

echo "=> Backup done"