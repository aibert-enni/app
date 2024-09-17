from django.db import models
from django.contrib.auth.models import User


class Institutes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название")
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)
    position = models.IntegerField(verbose_name="Позиция")

    class Meta:
        db_table = 'institutes'
        verbose_name_plural = "Институты"
        verbose_name = "Институт"
        managed = False

    def __str__(self):
        return self.name


# Create your models here.
class Numbers(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='ФИО сотрудника')
    position = models.CharField(max_length=255, null=True, verbose_name='Должность')
    cabinet = models.CharField(max_length=255, null=True, verbose_name='Кабинет')
    email = models.CharField(max_length=255, null=True, verbose_name='Почта', unique=True)
    institute = models.ForeignKey(Institutes, max_length=20, on_delete=models.SET_DEFAULT, default=1,
                                  verbose_name="Структура университета")
    local_number = models.CharField(max_length=255, null=True, verbose_name='Внутренний номер')
    telephone_number = models.CharField(max_length=255, null=True, verbose_name='Мобильный номер')
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

    class Meta:
        db_table = 'numbers'
        verbose_name_plural = "Номера"
        verbose_name = "Номер"
        managed = False

    def __str__(self):
        return self.name


class Logs(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

    class Meta:
        db_table = 'logs'
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        managed = False
