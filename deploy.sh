#!/bin/bash
set -e

REMOTE_HOST="marcika"
REMOTE_DIR="/var/www/webshop_eav_db"

echo "=== 1. Távoli könyvtár létrehozása ($REMOTE_HOST:$REMOTE_DIR) ==="
ssh $REMOTE_HOST "mkdir -p $REMOTE_DIR"

echo "=== 2. Projekt fájlok szinkronizálása rsync-cel ==="
rsync -avz --delete \
  --exclude 'mariadb_data' \
  --exclude '.git' \
  --exclude '__pycache__' \
  --exclude 'node_modules' \
  ./ $REMOTE_HOST:$REMOTE_DIR/

echo "=== 3. Éles .env beállítása a távoli szerveren ==="
ssh $REMOTE_HOST "cat << 'EOF' > $REMOTE_DIR/.env
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=webshop_eav_db
MYSQL_USER=webshop_user
MYSQL_PASSWORD=webshop_password
DOMAIN_PROD=db-milton.vane.hu
TRAEFIK_NETWORK=traefik
TRAEFIK_CERT_RESOLVER=myresolver
EOF"

echo "=== 4. Docker konténerek buildelése és indítása a szerveren ==="
ssh $REMOTE_HOST "cd $REMOTE_DIR && docker compose up -d --build"

echo "=== 5. Állapot ellenőrzése ==="
ssh $REMOTE_HOST "cd $REMOTE_DIR && docker compose ps"

echo "=========================================================="
echo "✅ Sikeres deploy! Elérhető: https://db-milton.vane.hu"
echo "=========================================================="
