#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -f ".venv/bin/activate" ]; then
  echo "Virtual environment not found at .venv/bin/activate" >&2
  exit 1
fi

source .venv/bin/activate

python -m pip install --upgrade build wheel setuptools
python -m build

echo "\nWheel build complete. dist contents:"
ls -1 dist
