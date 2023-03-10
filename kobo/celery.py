# coding: utf-8
import logging
import multiprocessing
import os

import celery
import constance
from django.apps import apps
from django.conf import settings

# http://celery.readthedocs.org/en/latest/django/first-steps-with-django.html

# Attempt to determine the project name from the directory containing this file
PROJECT_NAME = os.path.basename(os.path.dirname(__file__))

# Set the default Django settings module for the 'celery' command-line program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{}.settings.prod'.format(
    PROJECT_NAME))

Celery = celery.Celery

celery_app = Celery(PROJECT_NAME)
# Using a string here means the worker will not have to
# pickle the object when using Windows.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# The `celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)`
# technique described in
# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
# fails when INSTALLED_APPS includes a "dotted path to the appropriate
# AppConfig subclass" as recommended by
# https://docs.djangoproject.com/en/1.8/ref/applications/#configuring-applications.
# Ask Solem recommends the following workaround; see
# https://github.com/celery/celery/issues/2248#issuecomment-97404667
celery_app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
