#!/bin/bash
set -eux

echo "Setting up enviroment"

python3 -m venv .venv && source ./.venv/bin/activate \
&& pip install --upgrade pip && pip install -r requirements.txt

echo "Enviroment ready"