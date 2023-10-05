# coding=utf-8
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
    serverAddress = models.CharField('服务器地址', max_length=200, null=True)    # 非本地，必填服务器地址
    serverPort = models.IntegerField('端口', null=True)           # 非本地，则必填，只能是数据，最多10位
    createTime = models.DateTimeField('创建时间', auto_now=True)      # 自动获取当前时间

    class Meta:
        verbose_name = 'SeleniumHub管理'
        verbose_name_plural = 'SeleniumHub管理'

    def __str__(self):
        return self.serverName


class FrontPostManager(models.Model):
    name = models.CharField('名称', max_length=100)
    desc = models.CharField('描述', max_length=200)

    class Meta:
        verbose_name = '前置条件管理'
        verbose_name_plural = '前置条件管理'

    def __str__(self):
        return self.name


# 这里命令 对应 框架封装里面的命令
# 后面这一个就是页面显示内容
COMMANDS = (
    ('open', '打开'),
    ('send_keys', '输入'),
    ('clear', '清空'),
    ('click', '点击'),
    ('submit', '提交'),
    ('close', '关闭'),
    ('double_click', '双击'),
    ('drag_and_drop_to_object', '拖拽到对象'),
    ('execute_script', '执行脚本'),
    ('execute_async_script', '执行异步脚本'),
    ('mouse_over', '鼠标悬停'),
    ('pause', '等待'),
    ('select', '选择'),
    ('select_frame', '选择frame'),
    ('switch_to_parent_frame', '返回上级frame'),
    ('select_window', '选择窗口'),
    ('store', '存储'),
    ('store_text', '存储文本'),
    ('store_title', '存储标题'),
    ('store_value', '存储值'),
    ('store_xpath_count', '存储xpath总数'),
    ('add_cookie', '添加cookie'),
    ('wait_for_element_not_visible', '等待元素不可见'),
    ('wait_for_element_present', '待待元素发送'),
    ('wait_for_element_visible', '等待元素可见'),
    ('assert_variable', '断言变量'),
    ('assert_title_is', '断言标题是'),
    ('assert_title_contains', 'assert_title_包含'),
    ('assert_url_contains', 'assert_url_包含'),
    ('assert_url_matches', 'assert_url_匹配'),
    ('assert_url_to_be', 'assert_url_to_be'),
    ('assert_url_changes', 'assert_url_变化'),
    ('assert_presence_of_element_located', 'assert_presence_of_element_located'),
    ('assert_presence_of_all_elements_located', 'assert_presence_of_all_elements_located'),
    ('assert_visibility_of_element_located', 'assert_visibility_of_element_located'),
    ('assert_invisibility_of_element_located', 'assert_invisibility_of_element_located'),
    ('assert_invisibility_of_element', 'assert_invisibility_of_element'),
    ('assert_visibility_of', 'assert_visibility_of'),
    ('assert_visibility_of_any_elements_located', 'assert_visibility_of_any_elements_located'),
    ('assert_visibility_of_all_elements_located', 'assert_visibility_of_all_elements_located'),
    ('assert_element_to_be_clickable', 'assert_element_to_be_clickable'),
    ('assert_staleness_of', 'assert_staleness_of'),
    ('assert_text_to_be_present_in_element', 'assert_text_to_be_present_in_element'),
    ('assert_text_to_be_present_in_element_value', 'assert_text_to_be_present_in_element_value'),
    ('assert_frame_to_be_available_and_switch_to_it', 'assert_frame_to_be_available_and_switch_to_it'),
    ('assert_element_to_be_selected', 'assert_element_to_be_selected'),
    ('assert_element_located_to_be_selected', 'assert_element_located_to_be_selected'),
    ('assert_element_located_selection_state_to_be', 'assert_element_located_selection_state_to_be'),
    ('assert_number_of_windows_to_be', 'assert_number_of_windows_to_be'),
    ('assert_alert_is_present', 'assert_alert_is_present'),
    ('assert_text_of_alert', 'assert_text_of_alert')
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
    order = models.IntegerField('步骤', null=False, default=1)
    command = models.CharField('操作关键字', max_length=255, choices=COMMANDS)
    target = models.CharField('操作对象', max_length=255, null=True, blank=True)
    value = models.CharField('数据项', max_length=255, null=True, blank=True)
    desc = models.CharField('操作描述', max_length=255, blank=True)

    class Meta:
        verbose_name = '测试步骤'
        verbose_name_plural = '测试步骤'
        ordering = ('order',)

    def __str__(self):
        return ''

    # # 重构了数据库保存的save方法：在保存数据时，进行数据验证代码即可
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     """
    #     Save the current instance. Override this in a subclass if you want to
    #     control the saving process.
    #
    #     The 'force_insert' and 'force_update' parameters can be used to insist
    #     that the "save" must be an SQL insert or update (or equivalent for
    #     non-SQL backends), respectively. Normally, they should not be set.
    #     """
    #     self._prepare_related_fields_for_save(operation_name='save')
    #
    #     using = using or router.db_for_write(self.__class__, instance=self)
    #     if force_insert and (force_update or update_fields):
    #         raise ValueError("Cannot force both insert and updating in model saving.")
    #
    #     deferred_fields = self.get_deferred_fields()
    #     if update_fields is not None:
    #         # If update_fields is empty, skip the save. We do also check for
    #         # no-op saves later on for inheritance cases. This bailout is
    #         # still needed for skipping signal sending.
    #         if not update_fields:
    #             return
    #
    #         update_fields = frozenset(update_fields)
    #         field_names = set()
    #
    #         for field in self._meta.concrete_fields:
    #             if not field.primary_key:
    #                 field_names.add(field.name)
    #
    #                 if field.name != field.attname:
    #                     field_names.add(field.attname)
    #
    #         non_model_fields = update_fields.difference(field_names)
    #
    #         if non_model_fields:
    #             raise ValueError(
    #                 'The following fields do not exist in this model, are m2m '
    #                 'fields, or are non-concrete fields: %s'
    #                 % ', '.join(non_model_fields)
    #             )
    #
    #     # If saving to the same database, and this model is deferred, then
    #     # automatically do an "update_fields" save on the loaded fields.
    #     elif not force_insert and deferred_fields and using == self._state.db:
    #         field_names = set()
    #         for field in self._meta.concrete_fields:
    #             if not field.primary_key and not hasattr(field, 'through'):
    #                 field_names.add(field.attname)
    #         loaded_fields = field_names.difference(deferred_fields)
    #         if loaded_fields:
    #             update_fields = frozenset(loaded_fields)
    #
    #     # 可以在此处增加验证的断言代码
    #     print('order='+order)
    #
    #     # self.save_base(using=using, force_insert=force_insert,
    #     #                force_update=force_update, update_fields=update_fields)


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
