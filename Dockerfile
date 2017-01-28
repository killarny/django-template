FROM python:3.6

ENV CPATH /usr/local/include/python3.6m

RUN apt-get -qqy update && apt-get install -qqy \
    netcat-openbsd wget \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /
RUN pip install django
RUN bash -c "bash <(wget -qO- https://code.killarny.net/community/django-template/raw/master/bootstrap.sh) django_project"

WORKDIR /django_project
RUN pip install --no-cache-dir --src /usr/src -r requirements.txt

CMD ["bash", "/django_project/server/django-devserver.sh"]