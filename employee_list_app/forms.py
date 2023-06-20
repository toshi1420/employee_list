from datetime import date, timedelta
from django import forms
from django.core.validators import RegexValidator
from employee_list_app.models import Employee, Branch


class EmpForm(forms.ModelForm):
    date_of_entry = forms.DateField(widget=forms.SelectDateWidget(years=range(
        date.today().year - 50, date.today().year + 1)), label="入社日")

    def clean_date_of_entry(self):
        date_of_entry = self.cleaned_data["date_of_entry"]
        # date_of_entryが存在し、値が空でないことを確認する
        if date_of_entry >= date.today() + timedelta(days=1):
            raise forms.ValidationError(f"{date.today()}以降の日付は選択できません。")
        return date_of_entry

    class Meta:
        # モデル情報と紐付け
        model = Employee
        # 扱うフィールドを指定
        fields = ("emp_id", "name", "post", "date_of_entry", "branch")
        labels = {"emp_id": "社員番号", "name": "名前", "post": "役職", "date_of_entry": "入社日", "branch": "所属"}
        widgets = {
            "emp_id": forms.NumberInput(attrs={"min": 10000, "max": 19999}),
        }


class EmpSearchForm(forms.ModelForm):
    name = forms.CharField(required=False)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)

    class Meta:
        model = Employee
        fields = ("name", "branch")


class BranchForm(forms.ModelForm):
    tel_validator = RegexValidator(regex=r'^[0-9]+$', message="電話番号は'-'なしで半角数字のみ入力してください")
    # error_messages={"max_length": "12桁以下の数字を入力してください","min_length": "10桁以上の数字を入力してください。"}表示されない
    tel = forms.CharField(validators=[tel_validator], max_length=12, min_length=10, strip=True)

    def clean_tel(self):
        data = self.cleaned_data["tel"]
        if len(data) < 10:
            raise forms.ValidationError("10桁以上の数字を入力してください。")
        elif len(data) > 12:
            raise forms.ValidationError("12桁以下の数字を入力してください")
        return data

    class Meta:
        # モデル情報と紐付け
        model = Branch
        # 扱うフィールドを指定
        fields = ("name", "address", "tel")
        labels = {"name": "支社名", "address": "住所", "tel": "電話番号"}
