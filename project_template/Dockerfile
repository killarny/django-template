FROM python:3.6

ENV CPATH /usr/local/include/python3.6m

RUN apt-get -qqy update && apt-get install -qqy \
    netcat-openbsd wget nano \
	&& rm -rf /var/lib/apt/lists/*

RUN mkdir /{{ project_name }}
WORKDIR /{{ project_name }}

ADD requirements.txt /{{ project_name }}/
RUN pip install --no-cache-dir --src /usr/src -r requirements.txt

ADD . /{{ project_name }}
CMD ["bash", "/django_project/server/uwsgi.sh"]