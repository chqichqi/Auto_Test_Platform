# coding=utf-8
from django.contrib import admin

# Register your models here.
from simpleUi_app.models import TestReport


class TestReportAdmin(admin.ModelAdmin):
    list_display = ['created_time', 'report_type', 'title', 'desc', 'view_detail']
    list_display_links = None       # 禁用编辑按钮

    def has_add_permission(self, request):
        return False


admin.site.register(TestReport, TestReportAdmin)
