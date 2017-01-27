FROM python:3

ENV CPATH=/usr/local/include/python3.5m

RUN apt-get -qqy update && apt-get install -qqy \
    wget \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /
RUN pip install django
RUN bash -c "bash <(wget -qO- https://code.killarny.net/community/django-template/raw/master/bootstrap.sh) django_project"

WORKDIR /django_project
RUN pip install --no-cache-dir --src /usr/src -r requirements.txt