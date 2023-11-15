# coding=utf-8
from django.apps import AppConfig


class SimpleuiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simpleUi_app'
    verbose_name = '测试报告管理'

    # 保证在应用启动时加载信号处理函数
    def ready(self):
        import simpleUi_app.signals
