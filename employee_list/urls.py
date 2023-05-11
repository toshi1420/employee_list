from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls import include

# pathでappフォルダのurls.pyを読み込むためにinclude関数を記述
urlpatterns = [
    # 管理画面のPath
    path('admin/', admin.site.urls),
    # アプリケーション管理フォルダのurls.pyと関連づけるpath
    path('', include('employee_list_app.urls')),
]
