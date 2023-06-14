from datetime import date
from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Employee, Branch
from .forms import EmpForm, EmpSearchForm, BranchForm
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class Index(ListView):
    template_name = "employee_list/index.html"
    model = Employee
    context_object_name = "employees"
    ordering = "branch"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        form = EmpSearchForm(self.request.GET)
        if form.is_valid():
            # バリデーションを通ったデータはcleaned_dataに入るので "name", "branch"　を取り出す
            name = form.cleaned_data.get("name")
            branch = form.cleaned_data.get("branch")
            # name にデータがあれば　name に部分一致するデータを取り出す
            if name:
                queryset = queryset.filter(name__icontains=name)
            # branch にデータがあれば　branch に一致する　branch を取り出すが、djangoは外部キーフィールドに自動で_idを付けるので branch_id　になる
            if branch:
                queryset = queryset.filter(branch=branch)
        return queryset.select_related("branch")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = EmpSearchForm(self.request.GET)
        context["index_page"] = True
        return context

    # def get(self, request, *args, **kwargs):
    #     #   社員テーブルから全て取得
    #     employees = Employee.objects.all().order_by("branch")
    #     form = EmpSearchForm(request.GET)
    #     if form.is_valid():
    #         # バリデーションを通ったデータはcleaned_dataに入るので "name", "branch"　を取り出す
    #         name = form.cleaned_data.get("name")
    #         branch = form.cleaned_data.get("branch")
    #         # name にデータがあれば　name に部分一致するデータを取り出す
    #         if name:
    #             employees = employees.filter(name__icontains=name)
    #         # branch にデータがあれば　branch に一致する　branch を取り出すが、djangoは外部キーフィールドに自動で_idを付けるので branch_id　になる
    #         if branch:
    #             employees = employees.filter(branch_id=branch)
    #     context = {
    #         "employees": employees.select_related("branch"),
    #         "form": form
    #     }
    #     return render(request, "employee_list/index.html", context)


# def index(request):
#     # 社員テーブルから全て取得
#     employees = Employee.objects.select_related("branch").all().order_by("branch")
#     form = EmpSearchForm(request.GET)
#     if form.is_valid():
#         # バリデーションを通ったデータはcleaned_dataに入るので "name", "branch"　を取り出す
#         name = form.cleaned_data.get("name")
#         branch = form.cleaned_data.get("branch")
#         if name:
#             # name にデータがあれば　name に部分一致するデータを取り出す
#             employees = employees.select_related("branch").filter(name__contains=name)
#         if branch:
#             # branch にデータがあれば　branch に一致する　branch を取り出すが、djangoは外部キーフィールドに自動で_idを付けるので branch_id　になる
#             employees = employees.select_related("branch").filter(branch_id=branch)
#     return TemplateResponse(request, "employee_list/index.html",
#                             {"employees": employees,
#                              "form": form})


class EmpAdd(CreateView):
    template_name = "employee_list/emp_add.html"
    success_url = reverse_lazy("emp_add")
    form_class = EmpForm

    # fromに初期値を渡す
    def get_initial(self):
        initial = super().get_initial()
        if Employee.objects.exists():
            last_emp_id = Employee.objects.all().order_by("emp_id").last().emp_id + 1
        else:
            last_emp_id = 10000
        initial["emp_id"] = last_emp_id
        return initial

    # バリデーション成功時の処理
    def form_valid(self, form: EmpForm) -> HttpResponse:
        messages.success(self.request, "登録が完了しました")
        return super().form_valid(form)

    # バリデーション失敗時の処理
    def form_invalid(self, form: EmpForm) -> HttpResponse:
        return super().form_invalid(form)

# def emp_add(request):
#     if request.method == "GET":
#         if Employee.objects.exists():
#             last_emp_id = Employee.objects.all().order_by("emp_id").last().emp_id + 1
#         else:
#             last_emp_id = 10000
#         initial = {'emp_id': last_emp_id}
#         form = EmpForm(initial=initial)
#         return TemplateResponse(request, "employee_list/emp_add.html",
#                                 {"form": form})
#     # 社員追加のフォームがpostで来たら登録処理
#     else:
#         # requestで来たPOSTをモデルフォームへ
#         form = EmpForm(request.POST)
#         # バリデーション
#         if form.is_valid():
#             # データ新規追加
#             form.save()
#             messages.success(request, "登録が完了しました")
#             return HttpResponseRedirect(reverse("emp_add"))
#         return HttpResponseRedirect(reverse("emp_add"))


class EmpEdit(UpdateView):
    template_name = "employee_list/emp_edit.html"
    model = Employee
    form_class = EmpForm
    success_url = reverse_lazy("index")

    def form_valid(self, form: EmpForm) -> HttpResponse:
        messages.success(self.request, "更新が完了しました")
        return super().form_valid(form)

    def form_invalid(self, form: EmpForm) -> HttpResponse:
        messages.error(self.request, "更新できませんでした")
        return super().form_invalid(form)

# def emp_edit(request, pk):
#     try:
#         employee = Employee.objects.get(id=pk)
#     except Employee.DoesNotExist:
#         raise Http404
#     if request.method == "GET":
#         form = EmpForm(instance=employee)
#         return TemplateResponse(request, "employee_list/emp_edit.html",
#                                 {"employee": employee,
#                                  "form": form})
#     # requestPOSTをモデルフォームへ
#     else:
#         form = EmpForm(request.POST, instance=employee)
#         # バリデーション
#         if form.is_valid():
#             # データ上書き
#             form.save()
#             messages.success(request, "更新が完了しました")
#             return HttpResponseRedirect(reverse("index"))
#         return HttpResponseRedirect(reverse("index"))


@method_decorator(require_POST, name="dispatch")
class EmpDelete(DeleteView):
    model = Employee
    success_url = reverse_lazy("index")

    def form_valid(self, form) -> HttpResponse:
        messages.success(self.request, "データを削除しました")
        return super().form_valid(form)

# @require_POST
# def emp_delete(request, pk):
#     try:
#         employee = Employee.objects.get(id=pk)
#     except Employee.DoesNotExist:
#         raise Http404
#     employee.delete()
#     messages.success(request, "データを削除しました")
#     return HttpResponseRedirect(reverse("index"))


class BranchView(ListView):
    template_name = "employee_list/branch_view.html"
    model = Branch

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["branch_view_page"] = True
        return context

# def branch_view(request):
#     branchs = Branch.objects.all().order_by("id")
#     return TemplateResponse(request, "employee_list/branch_view.html",
#                             {"branchs": branchs})


class BranchEdit(UpdateView):
    template_name = "employee_list/branch_edit.html"
    model = Branch
    form_class = BranchForm
    success_url = reverse_lazy("index")

    def form_valid(self, form: BranchForm) -> HttpResponse:
        messages.success(self.request, "更新が完了しました")
        return super().form_valid(form)

    def form_invalid(self, form: BranchForm) -> HttpResponse:
        messages.error(self.request, "更新できませんでした")
        return super().form_invalid(form)


# def branch_edit(request, pk):
#     try:
#         branch = Branch.objects.get(id=pk)
#     except Branch.DoesNotExist:
#         raise Http404
#     if request.method == "GET":
#         form = BranchForm(instance=branch)
#         return TemplateResponse(request, "employee_list/branch_edit.html",
#                                 {"form": form,
#                                  "branch": branch})
#     else:
#         form = BranchForm(request.POST, instance=branch)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "更新が完了しました")
#             return HttpResponseRedirect(reverse("index"))
#         return HttpResponseRedirect(reverse("index"))

class BranchAdd(CreateView):
    template_name = "employee_list/branch_add.html"
    model = Branch
    form_class = BranchForm
    success_url = reverse_lazy("index")

    def form_valid(self, form: BranchForm) -> HttpResponse:
        messages.success(self.request, "登録が完了しました")
        return super().form_valid(form)

    def form_invalid(self, form: BranchForm) -> HttpResponse:
        messages.error(self.request, "登録できませんでした")
        return super().form_invalid(form)

# def branch_add(request):
#     if request.method == "GET":
#         form = BranchForm()
#         return TemplateResponse(request, "employee_list/branch_add.html",
#                                 {"form": form})
#     # 追加のフォームがpostで来たら登録処理
#     else:
#         # requestで来たPOSTをモデルフォームへ
#         form = BranchForm(request.POST)
#         # バリデーション
#         if form.is_valid():
#             # データ新規追加
#             form.save()
#             messages.success(request, "登録が完了しました")
#             return HttpResponseRedirect(reverse("index"))
#         return HttpResponseRedirect(reverse("branch_add"))


class BranchDelete(DeleteView):
    template_name = ""
    model = Branch
    success_url = reverse_lazy("index")

    def form_valid(self, form) -> HttpResponse:
        messages.success(self.request, "データを削除しました")
        return super().form_valid(form)


# @require_POST
# def branch_delete(request, pk):
#     try:
#         branch = Branch.objects.get(id=pk)
#     except Branch.DoesNotExist:
#         raise Http404
#     branch.delete()
#     messages.success(request, "データを削除しました")
#     return HttpResponseRedirect(reverse("index"))
