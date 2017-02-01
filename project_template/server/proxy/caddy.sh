#!/usr/bin/env bash
envsubst < /opt/src/Caddyfile.template 1>/opt/src/Caddyfile
if ! caddy -validate 2>/tmp/caddy-oops; then
    cat /tmp/caddy-oops
    exit 1
fi
caddy -agree -log=stdout