#!/bin/sh
set -e

mkdir -p "${DATA_DIR:-/app/data}"

if [ "${AUTO_SEED:-0}" = "1" ]; then
  python seed.py --if-empty
fi

exec "$@"
