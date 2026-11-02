#!/usr/bin/env bash
# Stop the FBA practical. Your notebooks stay in the practical/ folder.
cd "$(dirname "$0")"
docker compose down
