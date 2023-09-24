# coding=utf-8

# WebCaseStep
from django.forms import ModelForm, TextInput
from WebUiAtuoTest.models import WebCaseStep, CaseContext, DdtParams, FrontPostStep


class WebCaseStepForm(ModelForm):
    class Meta:
        model = WebCaseStep
        fields = ('order', 'command', 'target', 'value', 'desc',)
        widgets = {
            'order': TextInput(attrs={'size': 1, 'title': '请输入执行顺序'}),
            'target': TextInput(attrs={'size': 65, 'title': '请输入元素名'}),
            'value': TextInput(attrs={'size': 15, 'title': '请输入数据值'}),
            'desc': TextInput(attrs={'size': 30, 'title': '请输入说明'})
        }


class CaseContextForm(ModelForm):
    class Meta:
        model = CaseContext
        fields = ('argvName', 'argvValue',)
        widgets = {
            'argvName': TextInput(attrs={'size': 25, 'title': '请输入变量名'}),
            'argvValue': TextInput(attrs={'size': 75, 'title': '请输入变量值'}),
        }


class DdtParamsForm(ModelForm):
    class Meta:
        model = DdtParams
        fields = ('argvName', 'argvValue',)
        widgets = {
            'argvName': TextInput(attrs={'size': 25, 'title': '请输入参数名'}),
            'argvValue': TextInput(attrs={'size': 75, 'title': '请输入参数值'}),
        }


class FrontPostStepForm(ModelForm):
    class Meta:
        model = FrontPostStep
        fields = ('order', 'command', 'target', 'value', 'desc',)
        widgets = {
            'order': TextInput(attrs={'size': 1, 'title': '请输入执行顺序'}),
            'target': TextInput(attrs={'size': 65, 'title': '请输入元素名'}),
            'value': TextInput(attrs={'size': 15, 'title': '请输入数据值'}),
            'desc': TextInput(attrs={'size': 30, 'title': '请输入说明'})
        }
