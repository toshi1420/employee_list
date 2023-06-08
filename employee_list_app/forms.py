from datetime import date
from django import forms
# from django.core.validators import RegexValidator
from .models import Employee, Branch


class EmpForm(forms.ModelForm):
    class Meta:
        # モデル情報と紐付け
        model = Employee
        # 扱うフィールドを指定
        fields = ("emp_id", "name", "post", "date_of_entry", "branch")
        labels = {"emp_id": "社員番号", "name": "名前", "post": "役職", "date_of_entry": "入社日", "branch": "所属"}
        widgets = {
            "emp_id": forms.NumberInput(attrs={"min": 10000, "max": 19999}),
            "date_of_entry": forms.NumberInput(attrs={
                "type": "date", "max": date.today()
            })
        }


class EmpSearchForm(forms.ModelForm):
    name = forms.CharField(required=False)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)

    class Meta:
        model = Employee
        fields = ("name", "branch")


class BranchForm(forms.ModelForm):
    class Meta:
        # tel_regex = RegexValidator(regex=r'^[0-9]+$', message="電話番号は'-'なしで入力してください")
        # モデル情報と紐付け
        model = Branch
        # 扱うフィールドを指定
        fields = ("name", "address", "tel")
        labels = {"name": "支社名", "address": "住所", "tel": "電話番号"}
        # widgets = {
        #     "tel": forms.NumberInput(attrs={"min": 10, "max": 12, "valid": tel_regex})
        # }
