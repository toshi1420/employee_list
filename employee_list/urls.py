from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from users.views import SignupView, CustomLoginView
from django.contrib.auth.views import LogoutView
# pathでappフォルダのurls.pyを読み込むためにinclude関数を記述
urlpatterns = [
    # 管理画面のPath
    path('admin/', admin.site.urls),
    # ログアウト後のリダイレクト先をadminサイトと分ける
    path('accounts/logout/', LogoutView.as_view(next_page=settings.SITE_LOGOUT_REDIRECT_URL), name='logout'),
    path('admin/logout/', LogoutView.as_view(next_page=settings.ADMIN_LOGOUT_REDIRECT_URL), name='admin_logout'),
    # アプリケーション管理フォルダのurls.pyと関連づけるpath
    path('', include('employee_list_app.urls')),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    # authのテンプレートと関連付けるpath
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", SignupView.as_view(), name="signup"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
