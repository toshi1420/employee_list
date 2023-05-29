from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from users.views import SignupView

# pathでappフォルダのurls.pyを読み込むためにinclude関数を記述
urlpatterns = [
    # 管理画面のPath
    path('admin/', admin.site.urls),
    # アプリケーション管理フォルダのurls.pyと関連づけるpath
    path('', include('employee_list_app.urls')),
    # authのテンプレートと関連付けるpath
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", SignupView.as_view(), name="signup"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
