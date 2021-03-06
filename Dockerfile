FROM python:3.6

ENV CPATH /usr/local/include/python3.6m

RUN apt-get -qqy update && apt-get install -qqy \
    netcat-openbsd wget nano \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /
RUN pip install django
RUN bash -c "bash <(wget -qO- https://git.io/k.dj.start) django_project"

WORKDIR /django_project
RUN pip install --no-cache-dir --src /usr/src -r requirements.txt

# create links to the error pages in the proxy directory
RUN ln -s /django_project/server/proxy/*.html /django_project/django_project/templates/

CMD ["bash", "/django_project/server/uwsgi.sh"]