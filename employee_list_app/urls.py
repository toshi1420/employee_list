from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("emp_add", views.emp_add, name="emp_add"),
    path("emp_edit/<int:pk>/", views.emp_edit, name="emp_edit"),
    path("emp_delete/<int:pk>/", views.emp_delete, name="emp_delete"),
    path("branch_view", views.branch_view, name="branch_view"),
    path("branch_add", views.branch_add, name="branch_add"),
    path("branch_edit/<int:pk>", views.branch_edit, name="branch_edit"),
    path("branch_delete/<int:pk>", views.branch_delete, name="branch_delete"),
]
