FROM python:3

# detect and set the library include path for this version of python
RUN echo "export CPATH=$(find /usr/local/include -name python* |sort |head -n1)" >> ~/.bashrc

RUN apt-get -qqy update && apt-get install -qqy \
    wget \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /
RUN pip install django
RUN bash -c "bash <(wget -qO- https://code.killarny.net/community/django-template/raw/master/bootstrap.sh) django_project"

WORKDIR /django_project
RUN pip install --no-cache-dir --src /usr/src -r requirements.txt
