#!/bin/bash
# Script para arrancar el bot localmente en modo desarrollo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Verificar que existe el .env
if [ ! -f ".env" ]; then
    echo "ERROR: Falta el archivo .env"
    echo "Copiar .env.example a .env y completar los valores:"
    echo "  cp .env.example .env"
    exit 1
fi

# Verificar que existe el venv
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
    .venv/bin/pip install -r requirements-local.txt
fi

# Crear DBs si no existen
mkdir -p db
for db in discordusrs karma quotes; do
    if [ ! -f "db/${db}.db" ]; then
        echo "Creando DB vacia: db/${db}.db"
        touch "db/${db}.db"
    fi
done

# Inicializa schema minimo requerido por el bot
sqlite3 db/discordusrs.db "CREATE TABLE IF NOT EXISTS usuarios (username TEXT, user_id TEXT PRIMARY KEY, karma INTEGER DEFAULT 0, karmagiven INTEGER DEFAULT 0);"

echo "Iniciando BOFH bot en modo local..."
.venv/bin/python3 main.py
