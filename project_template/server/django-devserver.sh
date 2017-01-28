#!/usr/bin/env bash
until nc -z -v -w30 database 5432
do
  echo "Waiting for database container to start..."
  sleep 5
done
python /{{ project_name }}/manage.py migrate --noinput
python /{{ project_name }}/manage.py runserver 0.0.0.0:8000
