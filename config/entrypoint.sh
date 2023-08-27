#!/bin/bash
RUN_PORT="80"

gunicorn jobs.wsgi:application --bind "0.0.0.0:${RUN_PORT}" --access-logfile - --error-logfile -

#nginx -c /etc/nginx/conf.d/default.conf -g 'daemon off;'