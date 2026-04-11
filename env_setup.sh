#!/bin/bash
set -eux

echo "Setting up enviroment"

python3 -m venv .venv && source .venv/bin/activate \
&& pip install --upgrade pip && pip install -r requirements.txt

if [[ "$VIRTUAL_ENV" != "" ]]; then
	echo Virutal is activated
else
	echo ACTIVATING...
	source .venv/bin/activate
fi

echo "Enviroment ready"