#!/usr/bin/env bash
envsubst < /opt/src/Caddyfile.template 1>/opt/src/Caddyfile
caddy -agree -log=stdout