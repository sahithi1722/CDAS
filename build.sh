#!/usr/bin/env bash

pip install -r cdas/requirements.txt

python cdas/manage.py collectstatic --noinput

python cdas/manage.py migrate