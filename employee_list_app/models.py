from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class Branch(models.Model):
    name = models.CharField(max_length=30, verbose_name="支社名")
    address = models.CharField(max_length=255, verbose_name="住所")
    tel_regex = RegexValidator(regex=r'^[0-9]+$', message="電話番号は'-'なしで入力してください")
    tel = models.CharField(validators=[tel_regex], max_length=12, verbose_name="電話番号")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "支社"
        verbose_name_plural = "支社一覧"


class Employee(models.Model):
    emp_id = models.IntegerField(unique=True, validators=[MinValueValidator(
        10000), MaxValueValidator(19999)], verbose_name="社員番号")
    name = models.CharField(max_length=30, verbose_name="名前")
    post = models.CharField(max_length=30, null=True, blank=True, verbose_name="役職")
    date_of_entry = models.DateField(verbose_name="入社日")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, verbose_name="支社番号")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "社員"
        verbose_name_plural = "社員一覧"
