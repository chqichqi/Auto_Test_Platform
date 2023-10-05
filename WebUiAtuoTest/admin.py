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
from simpleUi_app.models import TestReport
from . import models, forms
# Register your models here.
from .models import CaseContext, DdtData, DdtParams, WebCaseStep, FrontPostManager, FrontPostStep, SeleniumHubServer, \
    Product


class ProductAdmin(admin.ModelAdmin):
    model = models.Product
    list_display = ['itemName', 'itemDesc', 'itemManager', 'createTime', 'id']
    list_display_links = ['itemName', 'itemDesc', 'itemManager', 'createTime', 'id']


admin.site.register(models.Product, ProductAdmin)


class SeleniumHubServerAdmin(admin.ModelAdmin):
    model = models.SeleniumHubServer
    list_display = ['id', 'serverName', 'serverType', 'serverAddress', 'serverPort', 'createTime']
    list_display_links = ['id', 'serverName', 'serverType', 'serverAddress', 'serverPort', 'createTime']


admin.site.register(models.SeleniumHubServer, SeleniumHubServerAdmin)


class FrontPostStepAdmin(admin.TabularInline):
    extra = 0
    model = models.FrontPostStep
    form = forms.FrontPostStepForm


# 前/后置管理
class FrontPostManagerAdmin(admin.ModelAdmin):
    model = models.FrontPostManager
    list_display = ['id', 'name', 'desc']
    list_display_links = ['id', 'name', 'desc']
    inlines = [FrontPostStepAdmin]


admin.site.register(models.FrontPostManager, FrontPostManagerAdmin)


class DdtParamsAdmin(nested_admin.NestedTabularInline):
    extra = 0
    model = models.DdtParams
    form = forms.DdtParamsForm


class DdtDataAdmin(nested_admin.NestedStackedInline):
    extra = 0
    model = models.DdtData
    inlines = [DdtParamsAdmin]


class CaseContextAdmin(nested_admin.NestedTabularInline):
    extra = 0
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
    list_per_page = 10    # 每页展示记录数
    ordering = ('created_time',)    # 创建时间升序排列
    actions = ['send_cases', 'run_case', ]

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
            modeladmin.send_yaml_file(modeladmin, clientRequest, queryset, path)
            # 执行测试用例 使用工具封装里面的webrun命令
            server = SeleniumHubServer.objects.filter(id=server_id).first()
            if str(server.serverType).__eq__("本地"):
                driver = server_browser
                print('本地')
            else:  # 远程
                driver = "REMOTE"
                print('远程')
            report_path = "/test_report/" + test_id
            test_code = subprocess.call("webrun --driver=" + driver
                                        + " --cases=" + path
                                        + " --report-path=" + report_path
                                        + " --host=" + server.serverAddress
                                        + " --port=" + str(server.serverPort)
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

    def send_yaml_file(self, modeladmin, clientRequest, queryset, path):
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
