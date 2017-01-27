#!/usr/bin/env bash
python /{{ project_name }}/manage.py migrate --noinput
python /{{ project_name }}/manage.py runserver 0.0.0.0:8000
