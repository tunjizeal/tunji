#!/bin/bash
set -e
source /etc/profile

# Run the main Celery worker (will not process low priority jobs).
# Start 2 processes by default; this will be overridden later, in Python code,
# according to the user's preference saved by django-constance
cd "${KPI_SRC_DIR}"

AUTOSCALE_MIN="${CELERY_AUTOSCALE_MIN:-2}"
AUTOSCALE_MAX="${CELERY_AUTOSCALE_MAX:-6}"

exec celery -A kobo worker --loglevel=info \
    --hostname=kpi_main_worker@%h \
    --logfile=${KPI_LOGS_DIR}/celery.log \
    --pidfile=/tmp/celery.pid \
    --queues=kpi_queue \
    --exclude-queues=kpi_low_priority_queue \
    --uid=${UWSGI_USER} \
    --gid=${UWSGI_GROUP} \
    --autoscale ${AUTOSCALE_MIN},${AUTOSCALE_MAX}
