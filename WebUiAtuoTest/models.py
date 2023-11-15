# coding=utf-8
import tkinter.messagebox
from tkinter import *
from django.core.exceptions import ValidationError
from django.db import models, router

# Create your models here.


class Product(models.Model):
    """
    配置项目/产品
    """
    itemName = models.CharField('项目名称', max_length=100)
    itemDesc = models.CharField('项目描述', max_length=200, null=True, blank=True)
    itemManager = models.CharField('项目负责人', max_length=30, null=True, blank=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)      # 自动获取当前时间

    class Meta:
        verbose_name = '项目管理'
        verbose_name_plural = '项目管理'

    def __str__(self):
        return self.itemName


SERVER_NAME = (
    ('本地', '本地'),
    ('REMOTE', '远程')
)


class SeleniumHubServer(models.Model):
    serverName = models.CharField('服务器名称', max_length=100)
    serverType = models.CharField('服务器类型', max_length=20, choices=SERVER_NAME)
    serverAddress = models.CharField('服务器地址', max_length=200, null=True, blank=True)    # 非本地，必填服务器地址
    serverPort = models.IntegerField('端口', null=True, blank=True)           # 非本地，则必填，只能是数据，最多10位
    createTime = models.DateTimeField('创建时间', auto_now=True)      # 自动获取当前时间

    class Meta:
        verbose_name = 'SeleniumHub管理'
        verbose_name_plural = 'SeleniumHub管理'

    def __str__(self):
        return self.serverName


class FrontPostManager(models.Model):
    # Product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="项目名称")
    name = models.CharField('名称+项目', max_length=100)
    desc = models.CharField('描述', max_length=200)

    class Meta:
        verbose_name = '前置条件管理'
        verbose_name_plural = '前置条件管理'

    def __str__(self):
        return self.name


# 这里命令 对应 框架封装里面的命令
# 后面这一个就是页面显示内容
COMMANDS = (
    ('open', '打开'),  # 无value、desc
    ('send_keys', '输入'),  # 无desc
    ('clear', '清空'),   # 无value、desc
    ('click', '点击'),    # 无desc
    ('submit', '提交'),   # 无value、desc
    ('close', '关闭'),      # 无target、value、desc
    ('double_click', '双击'),   # 无value、desc
    ('drag_and_drop_to_object', '拖拽到对象'),  # 无desc
    ('execute_script', '执行脚本'),  # 无desc
    ('execute_async_script', '执行异步脚本'),  # 无desc
    ('mouse_over', '鼠标悬停'),  # 无value、desc
    ('pause', '等待'),   # 无value、desc
    ('select', '选择'),  # 无desc
    ('select_frame', '选择frame'),  # 无value、desc
    ('switch_to_parent_frame', '返回上级frame'),  # 无target、value、desc
    ('select_window', '选择窗口'),  # 无value、desc
    ('store', '存储'),  # 无desc
    ('store_text', '存储文本'),  # 无desc
    ('store_title', '存储标题'),  # 无target、desc
    ('store_value', '存储值'),   # 无desc
    ('store_xpath_count', '存储xpath总数'),  # 无desc
    ('add_cookie', '添加cookie'),  # 无desc
    ('wait_for_element_not_visible', '等待元素不可见'),
    ('wait_for_element_present', '等待元素发送'),
    ('wait_for_element_visible', '等待元素可见'),
    ('assert_variable', '断言变量'),
    ('assert_title_is', '断言标题是'),               # 无target
    ('assert_title_contains', 'assert_title_包含'),  # 无target
    ('assert_url_contains', 'assert_url_包含'),     # 无target
    ('assert_url_matches', 'assert_url_匹配'),      # 无target
    ('assert_url_to_be', 'assert_url_to_be'),       # 无target
    ('assert_url_changes', 'assert_url_变化'),      # 无target
    ('assert_presence_of_element_located', 'assert_presence_of_element_located'),    # 无value
    ('assert_presence_of_all_elements_located', 'assert_presence_of_all_elements_located'),  # 无value
    ('assert_visibility_of_element_located', 'assert_visibility_of_element_located'),  # 无value
    ('assert_invisibility_of_element_located', 'assert_invisibility_of_element_located'),  # 无value
    ('assert_invisibility_of_element', 'assert_invisibility_of_element'),  # 无value
    ('assert_visibility_of', 'assert_visibility_of'),   # 无value
    ('assert_visibility_of_any_elements_located', 'assert_visibility_of_any_elements_located'), # 无value
    ('assert_visibility_of_all_elements_located', 'assert_visibility_of_all_elements_located'),  # 无value
    ('assert_element_to_be_clickable', 'assert_element_to_be_clickable'),  # 无value
    ('assert_staleness_of', 'assert_staleness_of'),   # 无value
    ('assert_text_to_be_present_in_element', 'assert_text_to_be_present_in_element'),
    ('assert_text_to_be_present_in_element_value', 'assert_text_to_be_present_in_element_value'),
    ('assert_frame_to_be_available_and_switch_to_it', 'assert_frame_to_be_available_and_switch_to_it'),  # 无value
    ('assert_element_to_be_selected', 'assert_element_to_be_selected'),  # 无value
    ('assert_element_located_to_be_selected', 'assert_element_located_to_be_selected'),  # 无value
    ('assert_element_located_selection_state_to_be', 'assert_element_located_selection_state_to_be'),  # 无value
    ('assert_number_of_windows_to_be', 'assert_number_of_windows_to_be'),  # 无target
    ('assert_alert_is_present', 'assert_alert_is_present'),     # 无target、value
    ('assert_text_of_alert', 'assert_text_of_alert')   # 无target
)


class FrontPostStep(models.Model):
    FrontPostManager = models.ForeignKey('FrontPostManager', on_delete=models.CASCADE, verbose_name="前置条件")
    order = models.IntegerField('步骤', null=False, default=1)
    command = models.CharField('操作关键字', max_length=255, choices=COMMANDS)
    target = models.CharField('操作对象',  max_length=255, null=True, blank=True)
    value = models.CharField('数据项',  max_length=255, null=True, blank=True)
    desc = models.CharField('操作描述', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = '前置用例'
        verbose_name_plural = '前置用例'
        ordering = ('order',)

    def __str__(self):
        return ''

    """
    "CHROME": webdriver.Chrome,
    "EDGE": webdriver.Edge,
    "FIREFOX": webdriver.Firefox,
    "IE": webdriver.Ie,
    "SAFARI": webdriver.Safari,
    "OPERA": webdriver.Opera,
    "PHANTOMJS": webdriver.PhantomJS,
    """


# 浏览器选项
BROWSER_CHOICE = (
    ('CHROME', '谷歌-chrome'),
    ('FIREFOX', '火狐-firefox'),
    ('IE', '微软-ie'),
    ('EDGE', '微软-edge'),
    ('OPERA', '奥普拉-opera'),
    # ('PHANTOMJS', '无头浏览器-phantomjs'),
    # ('SAFARI', '苹果-safari'),
)


class WebCase(models.Model):
    FrontPostManager = models.ForeignKey('FrontPostManager', on_delete=models.CASCADE,
                                         null=True, blank=True, verbose_name="前置用例步骤")
    Product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="所属项目")
    SeleniumHubServer = models.ForeignKey('SeleniumHubServer', on_delete=models.CASCADE,
                                          verbose_name="SeleniumServer服务器")
    caseName = models.CharField('用例名称', max_length=100)
    browser = models.CharField('浏览器', max_length=50, choices=BROWSER_CHOICE)
    created_time = models.DateTimeField('创建时间', auto_now=True)      # 自动获取当前时间

    class Meta:
        verbose_name = 'Web测试用例'
        verbose_name_plural = 'Web测试用例'

    def __str__(self):
        return self.caseName


class CaseContext(models.Model):
    WebCase = models.ForeignKey('WebCase', on_delete=models.CASCADE, verbose_name="测试用例")
    argvName = models.CharField('参数名', max_length=50)
    argvValue = models.CharField('参数值', max_length=1024)

    class Meta:
        verbose_name = '上下文参数定义'
        verbose_name_plural = '上下文参数定义'

    def __str__(self):
        return ''


class WebCaseStep(models.Model):
    WebCase = models.ForeignKey('WebCase', on_delete=models.CASCADE, verbose_name="用例前/后置条件")
    order = models.IntegerField('步骤', null=False, default=1, error_messages={"unique": '测试步骤序号不连续。'})
    command = models.CharField('操作关键字', max_length=255, choices=COMMANDS)
    target = models.CharField('操作对象', max_length=255, null=True, blank=True)
    value = models.CharField('数据项', max_length=255, null=True, blank=True)
    desc = models.CharField('操作描述', max_length=255, blank=True)
    flag = False
    v = 0

    class Meta:
        verbose_name = '测试步骤'
        verbose_name_plural = '测试步骤'
        ordering = ('order',)

    def __str__(self):
        return ''


class DdtData(models.Model):
    """
    数据驱动数据
    """
    WebCase = models.ForeignKey('WebCase', on_delete=models.CASCADE, verbose_name="测试用例")  # 关联测试用例
    desc = models.CharField('说明', max_length=255)

    class Meta:
        verbose_name = '数据驱动'
        verbose_name_plural = '数据驱动'

    def __str__(self):
        return ''


class DdtParams(models.Model):
    """
    数据驱动数据项
    """
    DdtData = models.ForeignKey('DdtData', on_delete=models.CASCADE, verbose_name="数据驱动项")  # 关联数据驱动项
    argvName = models.CharField('参数名', max_length=64)
    argvValue = models.CharField('参数值', max_length=1024)

    class Meta:
        verbose_name = '数据驱动数据项'
        verbose_name_plural = '数据驱动数据项'

    def __str__(self):
        return ''
