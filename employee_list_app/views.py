from django.template.response import TemplateResponse
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Employee, Branch
from .forms import EmpForm, EmpSearchForm, BranchForm


def index(request):
    # 社員テーブルから全て取得
    employees = Employee.objects.all().order_by("branch")
    form = EmpSearchForm(request.GET)
    if form.is_valid():
        # バリデーションを通ったデータはcleaned_dataに入るので "name", "branch"　を取り出す
        name = form.cleaned_data.get("name")
        branch = form.cleaned_data.get("branch")
        if name:
            # name にデータがあれば　name に部分一致するデータを取り出す
            employees = employees.filter(name__contains=name)
        if branch:
            # branch にデータがあれば　branch に一致する　branch を取り出すが、djangoは外部キーフィールドに自動で_idを付けるので branch_id　になる
            employees = employees.filter(branch_id=branch)
    return TemplateResponse(request, "employee_list/index.html",
                            {"employees": employees,
                             "form": form})


def emp_add(request):
    if request.method == "GET":
        form = EmpForm()
        return TemplateResponse(request, "employee_list/emp_add.html",
                                {"form": form})
    # 社員追加のフォームがpostで来たら登録処理
    else:
        # requestで来たPOSTをモデルフォームへ
        form = EmpForm(request.POST)
        # バリデーション
        if form.is_valid():
            # データ新規追加
            form.save()
            return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(reverse("emp_add"))


def emp_edit(request, pk):
    try:
        employee = Employee.objects.get(id=pk)
    except Employee.DoesNotExist:
        raise Http404
    if request.method == "GET":
        form = EmpForm(instance=employee)
        return TemplateResponse(request, "employee_list/emp_edit.html",
                                {"employee": employee,
                                 "form": form})
    # requestPOSTをモデルフォームへ
    else:
        form = EmpForm(request.POST, instance=employee)
        # バリデーション
        if form.is_valid():
            # データ上書き
            form.save()
            return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(reverse("index"))


@require_POST
def emp_delete(request, pk):
    try:
        employee = Employee.objects.get(id=pk)
    except Employee.DoesNotExist:
        raise Http404
    employee.delete()
    return HttpResponseRedirect(reverse("index"))


def branch_view(request):
    branchs = Branch.objects.all().order_by("id")
    return TemplateResponse(request, "employee_list/branch_view.html",
                            {"branchs": branchs})


def branch_edit(request, pk):
    try:
        branch = Branch.objects.get(id=pk)
    except Branch.DoesNotExist:
        raise Http404
    if request.method == "GET":
        form = BranchForm(instance=branch)
        return TemplateResponse(request, "employee_list/branch_edit.html",
                                {"form": form,
                                 "branch": branch})
    else:
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(reverse("index"))


def branch_add(request):
    if request.method == "GET":
        form = BranchForm()
        return TemplateResponse(request, "employee_list/branch_add.html",
                                {"form": form})
    # 追加のフォームがpostで来たら登録処理
    else:
        # requestで来たPOSTをモデルフォームへ
        form = BranchForm(request.POST)
        # バリデーション
        if form.is_valid():
            # データ新規追加
            form.save()
            return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(reverse("branch_add"))


@require_POST
def branch_delete(request, pk):
    try:
        branch = Branch.objects.get(id=pk)
    except Branch.DoesNotExist:
        raise Http404
    branch.delete()
    return HttpResponseRedirect(reverse("index"))
