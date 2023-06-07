from django.urls import path
from .views import (
    Index,
    EmpAdd,
    EmpEdit,
    EmpDelete,
    BranchView,
    BranchAdd,
    BranchEdit,
    BranchDelete
)


urlpatterns = [
    path("", Index.as_view(), name="index"),
    # path("", views.index, name="index"),
    path("emp_add/", EmpAdd.as_view(), name="emp_add"),
    # path("emp_add", views.emp_add, name="emp_add"),
    path("emp_edit/<int:pk>/", EmpEdit.as_view(), name="emp_edit"),
    # path("emp_edit/<int:pk>/", views.emmp_edit, name="emp_edit"),
    path("emp_delete/<int:pk>/", EmpDelete.as_view(), name="emp_delete"),
    # path("emp_delete/<int:pk>/", views.emp_delete, name="emp_delete"),
    path("branch_view/", BranchView.as_view(), name="branch_view"),
    # path("branch_view", views.branch_view, name="branch_view"),
    path("branch_add/", BranchAdd.as_view(), name="branch_add"),
    # path("branch_add", views.branch_add, name="branch_add"),
    path("branch_edit/<int:pk>/", BranchEdit.as_view(), name="branch_edit"),
    # path("branch_edit/<int:pk>", views.branch_edit, name="branch_edit"),
    path("branch_delete/<int:pk>/", BranchDelete.as_view(), name="branch_delete"),
    # path("branch_delete/<int:pk>", views.branch_delete, name="branch_delete"),
]
