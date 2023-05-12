import os

import environ

from .base import *  # noqa: F403

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))  # noqa: F405

DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
