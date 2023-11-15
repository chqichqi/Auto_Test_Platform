# coding=utf-8
import time

from django.contrib import admin
from datetime import datetime
import os
import subprocess
import uuid
import nested_admin
import yaml
from django.contrib import admin
from django.core.exceptions import ValidationError

from simpleUi_app.models import TestReport
from . import models, forms
# Register your models here.
from .models import CaseContext, DdtData, DdtParams, WebCaseStep, FrontPostManager, FrontPostStep, SeleniumHubServer, \
    Product, WebCase


def is_webCase_data_valid(formset):
    j = 1
    last_order = 0
    for form in formset:
        # 因为内联关系数据是一次性写入的，所以只需要在写入前对所有数据进行校验，从而不需要考虑是新增还是修改数据
        # 获取子对象（ChildModel）的字段数据
        child_field_data = form.cleaned_data.get('order')
        if not (form.cleaned_data.get('DELETE') or child_field_data is None):   # 只处理非勾选删除的记录
            print('order='+str(child_field_data))
            if j == 1:
                if child_field_data != 1:
                    raise ValidationError('第一步中的测试步骤序号不为1哈！')
            elif (child_field_data - 1) != last_order:
                raise ValidationError('第' + str(j) + '步测试步骤序号不连续，请重新输入哈！')
            child_field_command_data = form.cleaned_data.get('command')
            if child_field_command_data == '':
                raise ValidationError('第' + str(j) + '步操作关键字不为空，请重新选择哈！')
            if child_field_command_data.__contains__('assert_'):
                if not (child_field_command_data.__eq__('assert_alert_is_present') or
                        child_field_command_data.__eq__('assert_title_is') or
                        child_field_command_data.__eq__('assert_title_contains') or
                        child_field_command_data.__eq__('assert_url_contains') or
                        child_field_command_data.__eq__('assert_url_matches') or
                        child_field_command_data.__eq__('assert_url_to_be') or
                        child_field_command_data.__eq__('assert_url_changes') or
                        child_field_command_data.__eq__('assert_text_of_alert') or
                        child_field_command_data.__eq__('assert_number_of_windows_to_be')):
                    if form.cleaned_data.get('target') is None:
                        raise ValidationError('第' + str(j) + '步操作对象不能为空，请重新输入哈！')
                else:
                    if form.cleaned_data.get('value') is None:
                        raise ValidationError('第' + str(j) + '步操作数据项不能为空，请重新选择哈！')
            elif child_field_command_data.__eq__('open') or \
                    child_field_command_data.__eq__('execute_async_script') or \
                    child_field_command_data.__eq__('clear') or \
                    child_field_command_data.__eq__('select') or \
                    child_field_command_data.__eq__('submit') or \
                    child_field_command_data.__eq__('store') or \
                    child_field_command_data.__eq__('double_click') or \
                    child_field_command_data.__eq__('store_text') or \
                    child_field_command_data.__eq__('mouse_over') or \
                    child_field_command_data.__eq__('store_value') or \
                    child_field_command_data.__eq__('select_frame') or \
                    child_field_command_data.__eq__('store_xpath_count') or \
                    child_field_command_data.__eq__('select_window') or \
                    child_field_command_data.__eq__('add_cookie') or \
                    child_field_command_data.__eq__('click') or \
                    child_field_command_data.__eq__('wait_for_element_not_visible') or \
                    child_field_command_data.__eq__('send_keys') or \
                    child_field_command_data.__eq__('wait_for_element_present') or \
                    child_field_command_data.__eq__('drag_and_drop_to_object') or \
                    child_field_command_data.__eq__('wait_for_element_visible') or \
                    child_field_command_data.__eq__('execute_script'):
                if form.cleaned_data.get('target') is None:
                    raise ValidationError('第' + str(j) + '步操作对象不能为空，请重新输入哈！')
                elif child_field_command_data.__eq__('send_keys') or \
                        child_field_command_data.__eq__('store_value') or \
                        child_field_command_data.__eq__('drag_and_drop_to_object') or \
                        child_field_command_data.__eq__('store_xpath_count') or \
                        child_field_command_data.__eq__('execute_script') or \
                        child_field_command_data.__eq__('add_cookie') or \
                        child_field_command_data.__eq__('execute_async_script') or \
                        child_field_command_data.__eq__('wait_for_element_visible') or \
                        child_field_command_data.__eq__('select') or \
                        child_field_command_data.__eq__('wait_for_element_present') or \
                        child_field_command_data.__eq__('store') or \
                        child_field_command_data.__eq__('wait_for_element_visible') or \
                        child_field_command_data.__eq__('store_text'):
                    if form.cleaned_data.get('value') is None:
                        raise ValidationError('第' + str(j) + '步操作数据项不能为空，请重新选择哈！')
                    elif child_field_command_data.__eq__('wait_for_element_visible') or \
                            child_field_command_data.__eq__('wait_for_element_present') or \
                            child_field_command_data.__eq__('wait_for_element_visible'):
                        if form.cleaned_data.get('desc') is None:
                            raise ValidationError('第' + str(j) + '步操作描述项不能为空，请重新选择哈！')
            last_order = child_field_data   # 绑存本次测试步骤数据
        else:
            print('delete='+str(form.cleaned_data.get('order')))
        j += 1


def valid_data_and_save(request, change, all_obj, filed_name, count, tip_txt):
    if change:  # 修改数据
        for item in all_obj.values():
            if item[filed_name] == request.POST[filed_name]:
                raise ValidationError(tip_txt + '[' + request.POST[filed_name] + ']已存在，请重新输入哈！')
    else:  # 新增数据
        if count != 0:  # 主表
            raise ValidationError(tip_txt + '[' + request.POST[filed_name] + ']已存在，请重新输入哈！')


class ProductAdmin(admin.ModelAdmin):
    model = models.Product
    list_display = ['itemName', 'itemDesc', 'itemManager', 'createTime', 'id']
    list_display_links = ['itemName', 'itemDesc', 'itemManager', 'createTime', 'id']

    def save_model(self, request, obj, form, change):
        # 查询：select * from Product where id != obj.pk    obj.pk为主键ID
        all_obj = Product.objects.filter().exclude(id=obj.pk).all()
        count = Product.objects.filter(itemName=request.POST['itemName']).count()
        valid_data_and_save(request, change, all_obj, 'itemName', count, '项目管理中项目名称')

        super().save_model(request, obj, form, change)


admin.site.register(models.Product, ProductAdmin)


class SeleniumHubServerAdmin(admin.ModelAdmin):
    model = models.SeleniumHubServer
    list_display = ['serverName', 'serverType', 'serverAddress', 'serverPort', 'createTime']
    list_display_links = ['serverName', 'serverType', 'serverAddress', 'serverPort', 'createTime']

    # 验证ip地址是否合法
    def valid_ip(self, ip_address: str):
        if not ip_address.__contains__('.'):
            return False
        else:
            ip_split = ip_address.split('.')
            if len(ip_split) != 4:
                return False
            else:
                for n in ip_split:
                    if not n.isdigit():
                        return False
                    elif int(n) < 0 or int(n) > 255:
                        return False
        return True

    def valid_address_port(self, ip_address, port):
        if ip_address == '':
            raise ValidationError('SeleniumHub管理中服务器类型[远程]时，其服务地址不能为空哈！')
        else:
            if not self.valid_ip(ip_address):
                raise ValidationError('SeleniumHub管理中服务器地址存在非法！')
        if port == '':
            raise ValidationError('SeleniumHub管理中服务器类型[远程]时，其服务端口不能为空哈！')
        elif (not port.isdigit()) or int(port) > 65535:
            raise ValidationError('SeleniumHub管理中服务器端口存在非法！')

    def save_model(self, request, obj, form, change):
        # 查询：select * from SeleniumHubServer where id != obj.pk    obj.pk为主键ID
        all_obj = SeleniumHubServer.objects.filter().exclude(id=obj.pk).all()
        count = SeleniumHubServer.objects.filter(serverName=request.POST['serverName']).count()
        valid_data_and_save(request, change, all_obj, 'serverName', count, 'SeleniumHub管理中服务器名称')
        # 此处还要增加判断：serverType，若为远程，则'serverAddress', 'serverPort'不能为空
        if request.POST['serverType'] == 'REMOTE':
            self.valid_address_port(request.POST['serverAddress'], request.POST['serverPort'])

        super().save_model(request, obj, form, change)


admin.site.register(models.SeleniumHubServer, SeleniumHubServerAdmin)


class FrontPostStepAdmin(admin.TabularInline):
    extra = 1
    model = models.FrontPostStep
    form = forms.FrontPostStepForm


# 前置管理
class FrontPostManagerAdmin(admin.ModelAdmin):
    model = models.FrontPostManager
    list_display = ['name', 'desc']
    list_display_links = ['name', 'desc']
    inlines = [FrontPostStepAdmin]

    def save_model(self, request, obj, form, change):
        # 查询：select * from FrontPostManager where id != obj.pk    obj.pk为主键ID
        all_obj = FrontPostManager.objects.filter().exclude(id=obj.pk).all()
        count = FrontPostManager.objects.filter(name=request.POST['name']).count()
        valid_data_and_save(request, change, all_obj, 'name', count, '前置条件管理中前置名称')

        super().save_model(request, obj, form, change)

    # 关于内联结构的数据保存处理
    def save_formset(self, request, form, formset, change):
        # 在保存数据之前验证每个内联表单数据的合法性
        # 获取主对象（父模型）的字段数据
        # parent_field_data = form.cleaned_data.get('id')  # 替换为实际的字段名称
        if formset.is_valid() and formset.has_changed():
            is_webCase_data_valid(formset)

        super().save_formset(request, form, formset, change)


admin.site.register(models.FrontPostManager, FrontPostManagerAdmin)


class DdtParamsAdmin(nested_admin.NestedTabularInline):
    extra = 0
    model = models.DdtParams
    form = forms.DdtParamsForm


class DdtDataAdmin(nested_admin.NestedStackedInline):
    extra = 1
    model = models.DdtData
    inlines = [DdtParamsAdmin]


class CaseContextAdmin(nested_admin.NestedTabularInline):
    extra = 1
    model = models.CaseContext
    form = forms.CaseContextForm


class WebCaseStepAdmin(nested_admin.NestedTabularInline):
    extra = 1
    form = forms.WebCaseStepForm
    model = models.WebCaseStep


class WebCaseAdmin(nested_admin.NestedModelAdmin):
    model = models.WebCase
    inlines = [CaseContextAdmin, WebCaseStepAdmin, DdtDataAdmin]
    list_filter = ('Product', )
    list_display = ('caseName', 'Product', 'SeleniumHubServer', 'FrontPostManager', 'browser', 'created_time')
    list_display_links = ('caseName', 'Product', 'SeleniumHubServer', 'FrontPostManager', 'browser', 'created_time')
    # autocomplete_fields = ['SeleniumHubServer']
    # raw_id_fields = ['SeleniumHubServer']    # 显示外键的详细信息
    # readonly_fields = ['id']  # 仅读数据字段，即不能修改的数据
    list_per_page = 10    # 每页展示记录数
    ordering = ('created_time',)    # 创建时间升序排列
    actions = ['send_cases', 'run_case', ]

    # 定义自定义 CSS 样式
    class Media:
        css = {
            'all': ('/static/admin/custom_admin_styles.css',),
        }

    # 保存数据时，处理逻辑
    def save_model(self, request, obj, form, change):
        # 查询：select * from webcase where id != obj.pk   # obj.pk为主键ID
        all_obj = WebCase.objects.filter().exclude(id=obj.pk).all()
        count = WebCase.objects.filter(caseName=request.POST['caseName']).count()
        valid_data_and_save(request, change, all_obj, 'caseName', count, '测试用例名称')

        super().save_model(request, obj, form, change)

    def data_valid(self, formset, field_name, tip_txt):
        i = 1
        last_argv_name = ''
        for form in formset:
            child_field_name_data = form.cleaned_data.get(field_name)    # 参数名
            if child_field_name_data == '':
                raise ValidationError('第' + str(i) + '行' + '[' + tip_txt + ']不能为空哈！')
            elif i > 1 and last_argv_name == child_field_name_data:
                raise ValidationError('第' + str(i) + '行' + tip_txt + '[' + child_field_name_data + ']已存在，请重新输入哈！')
            last_argv_name = child_field_name_data
            i += 1

    def save_formset(self, request, form, formset, change):
        # 在保存数据之前验证每个内联表单数据的合法性
        # 在此处添加每个内联表单的验证逻辑
        if formset.is_valid() and formset.has_changed():
            if formset.model == CaseContext:  # This is ChildModelInline1
                self.data_valid(formset, 'argvName', '上下文参数定义中参数名')
            elif formset.model == WebCaseStep:  # This is ChildModelInline2
                is_webCase_data_valid(formset)
            elif formset.model == DdtData:  # This is ChildModelInline3
                self.data_valid(formset, 'argvName', '数据驱动数据项中参数名')

        super().save_formset(request, form, formset, change)

    @admin.action(permissions=['change'])
    def run_case(modeladmin, clientRequest, queryset):
        try:
            test_id = datetime.now().strftime("%Y%m%d%H%M%S")   # current date and time
            # 缓存服务配置文件，姑且认为多个用例均使用同一套服务
            server_id = queryset[0].SeleniumHubServer_id
            server_browser = queryset[0].browser
            product_id = queryset[0].Product_id
            print('product_id=' + str(product_id))
            product_obj = Product.objects.filter(id=product_id).first()
            print('case_name'+product_obj.itemName)
            path = './test_cases/'
            modeladmin.send_yaml_file(modeladmin, clientRequest, queryset, path, 1)
            # 执行测试用例 使用工具封装里面的webrun命令
            server = SeleniumHubServer.objects.filter(id=server_id).first()
            report_path = "/test_report/" + test_id
            if str(server.serverType).__eq__("本地"):
                driver = server_browser
                server_address = '127.0.0.1'
                server_port = '4444'
                print('本地')
            else:  # 远程
                driver = "REMOTE"
                server_address = server.serverAddress
                server_port = str(server.serverPort)
                print('远程')

            test_code = subprocess.call("webrun --driver=" + driver
                                        + " --cases=" + path
                                        + " --report-path=" + report_path
                                        + " --host=" + str(server_address)
                                        + " --port=" + str(server_port)
                                        + " --capability=" + server_browser,
                                        shell=True)
            if test_code == 0:
                test_stats = '成功'
            else:
                test_stats = '失败'
            # 保存测试记录及报告信息
            test_report = TestReport(
                title=product_obj.itemName,
                report_type="Web自动化测试",
                desc="执行状态:" + test_stats,
                report_detail=report_path + "/html/index.html"
            )
            test_report.save()
            # 测试完成后，将生成测试用例yaml文件全部删除
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))

        except Exception as e:
            modeladmin.message_user(clientRequest, e)
        else:
            modeladmin.message_user(clientRequest, '执行完毕，请前往指定页面查看测试报告')

    @admin.action(permissions=['change'])
    def send_cases(modeladmin, clientRequest, queryset):
        path = './test_cases_jenkins/'
        modeladmin.send_yaml_file(modeladmin, clientRequest, queryset, path)

    def send_yaml_file(self, modeladmin, clientRequest, queryset, path, do_type=0):
        try:
            # 每次生成yaml测试用例之前，将已经存在的测试用例yaml文件全部删除
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))

            product_id = queryset[0].Product_id
            print('product_id=' + str(product_id))
            product_obj = Product.objects.filter(id=product_id).first()
            # print('case_name' + product_obj.itemName)
            for k in range(len(queryset)):
                webcase = queryset[k]
                print("webcaseId=" + str(webcase.id))
                # 开始组装用例执行所需要的yaml文件，先组装dict, 再导出yaml
                caseinfo_dic = {}
                # 1.查询环境对应的变量信息
                context_dic = {}
                contexts = CaseContext.objects.filter(WebCase_id=webcase.id)
                for i in contexts:
                    context_dic.update({i.argvName: i.argvValue})
                # 每次都将测试用例的名称,当作变量:case_name的值写入上下文件当中
                context_dic['case_name'] = webcase.caseName

                caseinfo_dic.update({'context': context_dic})
                # 2. 查询数据驱动信息
                ddt_list = []
                ddt_datas = DdtData.objects.filter(WebCase_id=webcase.id)
                for item in ddt_datas:
                    ddt_dic = {'desc': item.desc}
                    dps = DdtParams.objects.filter(DdtData_id=item.id)
                    for dp in dps:
                        ddt_dic.update({dp.argvName: dp.argvValue})
                    ddt_list.append(ddt_dic)

                caseinfo_dic.update({'ddts': ddt_list})

                # 3. 查询测试步骤信息
                step_list = []
                case_steps = WebCaseStep.objects.filter(WebCase_id=webcase.id)
                for s in case_steps:
                    step_dic = {}
                    # 1.基本信息
                    step_dic.update({
                        "command": s.command,
                        "desc": s.desc,
                        "target": s.target,
                        "value": s.value
                    })
                    step_list.append(step_dic)

                # 添加前置条件流程
                pid = webcase.FrontPostManager_id
                print('pid=' + str(pid))
                if pid is not None:  # 表示没有前/后置条件
                    p_case = FrontPostManager.objects.filter(id=pid).first()
                    print('p_case.id=' + str(p_case.id))
                    if p_case.id is not None:
                        p_step_list = []
                        p_case_steps = FrontPostStep.objects.filter(FrontPostManager_id=p_case.id)
                        print('len=' + str(p_case_steps.__len__()))

                        for s in p_case_steps:
                            step_dic = {}
                            step_dic.update({
                                "command": s.command,
                                "desc": s.desc,
                                "target": s.target,
                                "value": s.value
                            })
                            p_step_list.append(step_dic)
                        step_list = p_step_list + step_list
                        print('step_list' + str(step_list))

                print('steps=' + str(step_list))
                caseinfo_dic.update({'steps': step_list})
                print("caseinfo_dic=" + str(caseinfo_dic))

                # 导出执行信息到临时文件
                file_name = path + "/test_" + product_obj.itemName + "_" + webcase.caseName + ".yaml"
                print("filename=" + file_name)
                if not os.path.exists(path):
                    os.makedirs(path)
                w_file = open(file_name, "w+", encoding='utf-8')
                yaml.dump(caseinfo_dic, w_file, encoding='utf-8', allow_unicode=True)
                w_file.close()
                print('yaml write success')
        except Exception as e:
            modeladmin.message_user(clientRequest, e)
        else:
            if do_type == 0:
                modeladmin.message_user(clientRequest, '生成测试用例完毕')

    send_cases.short_description = '仅生成供CI/CD使用的测试用例'
    send_cases.confirm = '生成用例需要一定时间，请耐心等待，勿重复点击'
    send_cases.type = 'warning'  # 绿色

    run_case.short_description = ' << 执行测试用例 >> '
    run_case.confirm = '执行用例需要一定时间，请耐心等待，勿重复点击'
    run_case.type = 'success'     # 绿色
    # run_case.icon = 'fas fa-lock-open'   # 锁开状态
    # run_case.icon = 'fas fa-backward'    # 锁开状态


admin.site.register(models.WebCase, WebCaseAdmin)
