from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import redirect
# Register your models here.
from .models import Numbers, Institutes, Logs


class CustomAdminSite(admin.AdminSite):
    site_header = "Мой админский сайт"

    def index(self, request, extra_context=None):
        if not extra_context:
            extra_context = {}
        if not request.user.is_superuser:  # Пример условного отображения для суперпользователей
            return redirect('admin:app_numbers_changelist')
        return super().index(request, extra_context=extra_context)


admin_site = CustomAdminSite(name='custom_admin')


class NumberAdminForm(forms.ModelForm):
    class Meta:
        model = Numbers
        fields = ['institute', 'email', 'name', 'position', 'cabinet', 'local_number', 'telephone_number']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].required = False
        self.fields['cabinet'].required = False
        self.fields['email'].required = False
        self.fields['local_number'].required = False
        self.fields['telephone_number'].required = False


class NumberAdmin(admin.ModelAdmin):
    form = NumberAdminForm

    change_list_template = 'admin/number_change_list.html'

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        return super(NumberAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        # Подготовьте ваш контекст
        context = {
            'custom_variable': 'Custom Value',
            # Вы можете добавить другие переменные в контекст
        }

        # Объедините с контекстом по умолчанию
        if extra_context:
            context.update(extra_context)

        # Вызовите родительский метод с правильными аргументами
        return super().changelist_view(request, extra_context=context)

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Numbers.objects.get(pk=obj.pk)
            Logs.objects.create(user=request.user, text=f"""
                Пользователь {request.user.username.capitalize()}: Обновил номер: <br><b class="ml-2">внутренний номер:</b> {old_obj.local_number} => {obj.local_number}, <br><b class="ml-2">фио:</b> {old_obj.name} => {obj.name}, <br><b class="ml-2">должность:</b> {old_obj.position} => {obj.position}, <br><b class="ml-2">кабинет:</b> {old_obj.cabinet} => {obj.cabinet}, <br><b class="ml-2">почта:</b> {old_obj.email} => {obj.email}, <br><b class="ml-2">телефон:</b> {old_obj.telephone_number} => {obj.telephone_number}
            """)
        else:
            Logs.objects.create(user=request.user, text=f"""
                        Пользователь {request.user.username.capitalize()}: Создал номер: <br><b class="ml-2">внутренний номер:</b> {obj.local_number}, <br><b class="ml-2">фио:</b> {obj.name}, <br><b class="ml-2">должность:</b> {obj.position}, <br><b class="ml-2">кабинет:</b> {obj.cabinet}, <br><b class="ml-2">почта:</b> {obj.email}, <br><b class="ml-2">телефон:</b> {obj.telephone_number}
                    """)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Логика перед удалением объекта
        Logs.objects.create(user=request.user, text=f"""
                                Пользователь {request.user.username.capitalize()}: Удалил номер: <br><b class="ml-2">внутренний номер:</b> {obj.local_number}, <br><b class="ml-2">фио:</b> {obj.name}, <br><b class="ml-2">должность:</b> {obj.position}, <br><b class="ml-2">кабинет:</b> {obj.cabinet}, <br><b class="ml-2">почта:</b> {obj.email}, <br><b class="ml-2">телефон:</b> {obj.telephone_number}
                            """)
        # Удаление объекта
        super().delete_model(request, obj)


class InstituteAdminForm(forms.ModelForm):
    class Meta:
        model = Institutes
        fields = ["name", "position"]


class InstitutesAdmin(admin.ModelAdmin):
    form = InstituteAdminForm

    change_list_template = 'admin/institute_change_list.html'

    def changelist_view(self, request, extra_context=None):
        context = {}

        if extra_context:
            context.update(extra_context)

        return super().changelist_view(request, extra_context=context)

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Institutes.objects.get(pk=obj.pk)
            Logs.objects.create(user=request.user, text=f"""
                Пользователь {request.user.username.capitalize()}: Обновил Институт: <br><b class="ml-2">Название:</b> {old_obj.name} => {obj.name}
            """)
        else:
            Logs.objects.create(user=request.user, text=f"""
                        Пользователь {request.user.username.capitalize()}: Создал Институт: <br><b class="ml-2">Название:</b> {obj.name}
                        """)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Логика перед удалением объекта
        Logs.objects.create(user=request.user, text=f"""
                                Пользователь {request.user.username.capitalize()}: Удалил Институт: <br><b class="ml-2">Название:</b> {obj.local_number}
                """)
        # Удаление объекта
        super().delete_model(request, obj)


class LogsAdmin(admin.ModelAdmin):
    change_list_template = 'admin/logs_change_list.html'

    def changelist_view(self, request, extra_context=None):
        context = {}

        if extra_context:
            context.update(extra_context)

        return super().changelist_view(request, extra_context=context)

    ordering = ('created_at',)


admin_site.register(Numbers, NumberAdmin)
admin_site.register(User)
admin_site.register(Institutes, InstitutesAdmin)
admin_site.register(Logs, LogsAdmin)
