from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ['debug_toolbar',]  # noqa: F405

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]  # noqa: F405

INTERNAL_IPS += ['127.0.0.1',]  # noqa: F405
