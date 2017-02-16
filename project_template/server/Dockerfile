FROM python:3.6

ENV CPATH /usr/local/include/python3.6m

RUN apt-get -qqy update && apt-get install -qqy \
    netcat-openbsd wget \
	&& rm -rf /var/lib/apt/lists/*


##############################################################################
# ssh deploy key(s)
# NOTE: copy/hardlink the deploy key into the directory containing this Dockerfile
ADD deploy-key .
RUN mkdir -p /root/.ssh/
RUN mv deploy-key /root/.ssh/id_rsa
RUN chown root:root /root/.ssh/id_rsa
RUN chmod 0600 /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan -T 60 code.alt.net >> /root/.ssh/known_hosts


##############################################################################
# set project branch, and clone repo
ARG REPO_URL
ENV REPO_URL ${REPO_URL}
ARG BRANCH
ENV BRANCH ${BRANCH:-master}
RUN git clone -b ${BRANCH} ${REPO_URL} /{{ project_name }}


##############################################################################
# install project deps
RUN pip install --no-cache-dir --src /usr/src -r /{{ project_name }}/requirements.txt


##############################################################################
# make logging, media, and runtime directories
RUN mkdir -p /var/log/{{ project_name }}
RUN chown www-data:www-data -R /var/log/{{ project_name }}/
RUN mkdir -p /var/media/{{ project_name }}/media/
RUN chown www-data:www-data -R /var/media/{{ project_name }}/media/
RUN mkdir -p /var/media/{{ project_name }}/static/
RUN chown www-data:www-data -R /var/media/{{ project_name }}/static/
RUN mkdir -p /var/run/{{ project_name }}/
RUN chown www-data:www-data -R /var/run/{{ project_name }}/


##############################################################################
# run the server
WORKDIR /{{ project_name }}
CMD ["bash", "/{{ project_name }}/server/uwsgi.sh"]