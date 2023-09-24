# coding=utf-8
import socket
from django.db import models
from django.utils.html import format_html


# Create your models here.
class TestReport(models.Model):
    title = models.CharField('报告标题', max_length=1024)
    report_type = models.CharField(verbose_name='报告类型', max_length=200, null=True)
    desc = models.CharField('报告简述', max_length=1024)
    report_detail = models.CharField('报告详情', max_length=1024)
    created_time = models.DateTimeField('报告生成时间', auto_now=True)

    class Meta:
        verbose_name = '测试报告'
        verbose_name_plural = '测试报告列表'

    def __str__(self):
        return self.title

    # 记录后面自定义按钮
    def view_detail(self):
        # btn_str = '<input name="view_detail" onclick="javascript:window.open(window.location.protocol +\'//\' + window.location.host + \'{}\');" ' \
        #           'type="button" id="btn_assign_{}" ' \
        #           'value="查看测试报告详情">'.format("/django_simpleUi"+self.report_detail, self.id)
        host_name = socket.gethostname()
        print('host_name=' + str(host_name))
        ip = socket.gethostbyname(host_name)
        print('ip=' + str(ip))
        ip = 'localhost'
        btn_str = '<input name="view_detail" onclick="javascript:window.open(window.location.protocol +\'//' +\
                  ip+':63342{}\');" type="button" id="btn_assign_{}" ' \
                  'value="查看测试报告详情">'.format("/django_simpleUi"+self.report_detail, self.id)
        return format_html(btn_str)

    view_detail.short_description = ('操作')
    view_detail.type = 'success'
