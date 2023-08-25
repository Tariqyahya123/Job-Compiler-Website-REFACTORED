#!/bin/bash
RUN_PORT="8000"

gunicorn jobs.wsgi:application --bind "0.0.0.0:${RUN_PORT}" --access-logfile - --error-logfile - --daemon

nginx -c /etc/nginx/conf.d/default.conf -g 'daemon off;'