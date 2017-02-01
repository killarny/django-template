FROM debian:stable

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    gettext-base wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/bin
RUN wget -qO- "https://caddyserver.com/download/build?os=linux&arch=amd64&features=" | tar zx
RUN chmod +x caddy

RUN mkdir -p /opt/src/
WORKDIR /opt/src/
COPY Caddyfile Caddyfile.template
COPY caddy.sh .

CMD ["bash", "caddy.sh"]