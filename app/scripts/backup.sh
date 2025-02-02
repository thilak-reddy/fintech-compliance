#!/bin/bash
# SOC2-3: Backup script
TIMESTAMP=$(date +%Y%m%d%H%M)
BACKUP_DIR="/app/backup"
SOURCE_DIR="/app/data"

tar -czf $BACKUP_DIR/backup_$TIMESTAMP.tar.gz $SOURCE_DIR
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete