import os
from django.contrib.messages import constants as messages
from pathlib import Path
# django-environをインポート
import environ

# BASE_DIRを指定する。（environのところで必要なため記述）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# environの設定をする
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

# シークレットキーを環境変数から引っ張る。
SECRET_KEY = env("SECRET_KEY")

# 本番環境ではFasleに変更。
DEBUG = False
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Tepmpateフォルダへの絶対パスを定義
TEMPLATE_DIR = BASE_DIR / "Template"

# staticフォルダへの絶対パスを定義
STATIC_DIR = BASE_DIR / "static"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'users',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'employee_list_app',
    # 'django.contrib.sites',  # allauth
    # 'allauth',  # allauth
    # 'allauth.account',  # allauth
    # 'allauth.socialaccount',  # allauth
    'widget_tweaks',
]
# django.contrib.sites用のサイト識別IDを設定
# SITE_ID = 1
# 認証バックエンドの設定
# AUTHENTICATION_BACKENDS = [
#     'allauth.account.auth_backends.AuthenticationBackend',  # 一般ユーザー用(メールアドレス認証)
#     'django.contrib.auth.backends.ModelBackend',  # 管理サイト用(ユーザー名認証)
# ]

# ACCOUNT_AUTHENTICATION_METHOD = 'email'  # メールアドレス認証に変更する設定
# ACCOUNT_USERNAME_REQUIRED = False  # サインナップ、ログイン時のユーザーネーム認証をキャンセル

# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # サインアップにメールアドレス確認を使用
# ACCOUNT_EMAIL_REQUIRED = True  # ユーザー登録画面でメールアドレスを必須項目に

EMAIL_BACKEND = ''

LOGIN_REDIRECT_URL = '/'  # ログイン成功後の遷移先の指定
SITE_LOGOUT_REDIRECT_URL = '/accounts/login/'  # ログアウト成功後の遷移先の指定 allauathはACCOUNTS_を付ける
LOGIN_URL = '/accounts/login/'  # 非ログイン状態でアクセスした際のリダイレクト先
ADMIN_LOGOUT_REDIRECT_URL = "/admin/login/"  # adminサイトからログアウトした時のリダイレクト先
# ACCOUNT_LOGOUT_ON_GET = True  # 確認を行わずログアウトする設定

AUTH_USER_MODEL = "users.EmpListUser"  # 認証時に、参照するユーザーモデルを指定する

# ACCOUNT_FORMS = {"signup": "users.forms.SignupForm"}

INTERNAL_IPS = []

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'global_login_required.GlobalLoginRequiredMiddleware',
]

ROOT_URLCONF = 'employee_list.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],  # 追加
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'employee_list.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

MESSAGE_TAGS = {
    messages.INFO: 'alert alert-info',
    messages.SUCCESS: 'alert alert-success',
    messages.WARNING: 'alert alert-warning',
    messages.ERROR: 'alert alert-danger',
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFIELES_DIRS = [
    STATIC_DIR,
]

PUBLIC_PATHS = [
    "/admin/",
    "/accounts/login/",
    "/signup/",
    "/accounts/password_reset/",
    "/accounts/reset/",
]
