from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ['debug_toolbar',]  # noqa: F405

MIDDLEWARE += [  # noqa: F405
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS += ['127.0.0.1',]  # noqa: F405

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # ローカルでの開発のためメールをコンソールで表示する
