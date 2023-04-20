from django import forms

from .models import Employee, Branch


class EmpForm(forms.ModelForm):
    class Meta:
        # モデル情報と紐付け
        model = Employee
        fields = ("emp_id", "name", "post", "date_of_entry", "branch")  # 扱うフィールドを指定
        labels = {"emp_id": "社員番号", "name": "名前", "post": "役職", "date_of_entry": "入社日", "branch": "所属"}
        widgets = {
            'date_of_entry': forms.NumberInput(attrs={
                "type": "date"
            })
        }


class EmpSearchForm(forms.ModelForm):
    name = forms.CharField(label="名前", required=False)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), label="支社", required=False)

    class Meta:
        model = Employee
        fields = ("name", "branch")
        # labels = {"name": "名前", "branch": "支社名"}


class BranchForm(forms.ModelForm):
    class Meta:
        # モデル情報と紐付け
        model = Branch
        # 扱うフィールドを指定
        fields = ("name", "address", "tel")
        labels = {"name": "支社名", "address": "住所", "tel": "電話番号"}
