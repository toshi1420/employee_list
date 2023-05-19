from django.conf import settings
from django.contrib import admin
from django.urls import path, include

# pathでappフォルダのurls.pyを読み込むためにinclude関数を記述
urlpatterns = [
    # 管理画面のPath
    path('admin/', admin.site.urls),
    # アプリケーション管理フォルダのurls.pyと関連づけるpath
    path('', include('employee_list_app.urls')),
    # allauthのテンプレートと関連付けるpath
    path("account/", include("allauth.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
