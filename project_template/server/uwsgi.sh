#!/usr/bin/env bash
until nc -z -v -w30 database 5432 > /dev/null 2>&1
do
  echo "Waiting for database container to start..."
  sleep 5
done
python /{{ project_name }}/manage.py collectstatic -v0 --noinput
python /{{ project_name }}/manage.py migrate --noinput
uwsgi /{{ project_name }}/server/uwsgi.ini
