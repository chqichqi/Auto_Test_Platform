# Generated by Django 3.2.20 on 2023-09-20 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DdtData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=255, verbose_name='说明')),
            ],
            options={
                'verbose_name': '数据驱动',
                'verbose_name_plural': '数据驱动列表',
            },
        ),
        migrations.CreateModel(
            name='FrontPostManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('desc', models.CharField(max_length=200, verbose_name='描述')),
            ],
            options={
                'verbose_name': '前/后置条件管理',
                'verbose_name_plural': '前/后置条件管理列表',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemName', models.CharField(max_length=100, verbose_name='项目名称')),
                ('itemDesc', models.CharField(blank=True, max_length=200, null=True, verbose_name='项目描述')),
                ('itemManager', models.CharField(blank=True, max_length=30, null=True, verbose_name='项目负责人')),
                ('createTime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '项目管理',
                'verbose_name_plural': '项目管理列表',
            },
        ),
        migrations.CreateModel(
            name='SeleniumHubServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serverName', models.CharField(max_length=100, verbose_name='服务器名称')),
                ('serverType', models.CharField(choices=[('本地', '本地'), ('REMOTE', '远程')], max_length=20, verbose_name='服务器类型')),
                ('serverAddress', models.CharField(max_length=200, null=True, verbose_name='服务器地址')),
                ('serverPort', models.IntegerField(null=True, verbose_name='端口')),
                ('createTime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'seleniumHub管理',
                'verbose_name_plural': 'seleniumHub管理列表',
            },
        ),
        migrations.CreateModel(
            name='WebCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caseName', models.CharField(max_length=100, verbose_name='用例名称')),
                ('browser', models.CharField(choices=[('CHROME', '谷歌-chrome'), ('FIREFOX', '火狐-firefox'), ('IE', '微软-ie'), ('EDGE', '微软-edge'), ('OPERA', '奥普拉-opera')], max_length=50, verbose_name='浏览器')),
                ('FrontPostManager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='WebUiAutoTest.frontpostmanager', verbose_name='前/后置用例步骤')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebUiAutoTest.product', verbose_name='所属项目')),
                ('SeleniumHubServer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebUiAutoTest.seleniumhubserver', verbose_name='SeleniumServer服务器')),
            ],
            options={
                'verbose_name': 'WEB测试用例',
                'verbose_name_plural': 'WEB测试用例列表',
            },
        ),
        migrations.CreateModel(
            name='WebCaseStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1, verbose_name='执行顺序')),
                ('command', models.CharField(choices=[('click', '点击'), ('close', '关闭'), ('double_click', '双击'), ('drag_and_drop_to_object', '拖拽到对象'), ('execute_script', '执行脚本'), ('execute_async_script', '执行异步脚本'), ('mouse_over', '鼠标悬停'), ('open', '打开'), ('pause', '等待'), ('select', '选择'), ('select_frame', '选择frame'), ('switch_to_parent_frame', '返回上级frame'), ('select_window', '选择窗口'), ('send_keys', '输入'), ('store', '存储'), ('store_text', '存储文本'), ('store_title', '存储标题'), ('store_value', '存储值'), ('store_xpath_count', '存储xpath总数'), ('add_cookie', '添加cookie'), ('submit', '提交'), ('wait_for_element_not_visible', '等待元素不可见'), ('wait_for_element_present', '待待元素发送'), ('wait_for_element_visible', '等待元素可见'), ('assert_variable', '断言变量'), ('assert_title_is', '断言标题是'), ('assert_title_contains', 'assert_title_包含'), ('assert_url_contains', 'assert_url_包含'), ('assert_url_matches', 'assert_url_匹配'), ('assert_url_to_be', 'assert_url_to_be'), ('assert_url_changes', 'assert_url_变化'), ('assert_presence_of_element_located', 'assert_presence_of_element_located'), ('assert_presence_of_all_elements_located', 'assert_presence_of_all_elements_located'), ('assert_visibility_of_element_located', 'assert_visibility_of_element_located'), ('assert_invisibility_of_element_located', 'assert_invisibility_of_element_located'), ('assert_invisibility_of_element', 'assert_invisibility_of_element'), ('assert_visibility_of', 'assert_visibility_of'), ('assert_visibility_of_any_elements_located', 'assert_visibility_of_any_elements_located'), ('assert_visibility_of_all_elements_located', 'assert_visibility_of_all_elements_located'), ('assert_element_to_be_clickable', 'assert_element_to_be_clickable'), ('assert_staleness_of', 'assert_staleness_of'), ('assert_text_to_be_present_in_element', 'assert_text_to_be_present_in_element'), ('assert_text_to_be_present_in_element_value', 'assert_text_to_be_present_in_element_value'), ('assert_frame_to_be_available_and_switch_to_it', 'assert_frame_to_be_available_and_switch_to_it'), ('assert_element_to_be_selected', 'assert_element_to_be_selected'), ('assert_element_located_to_be_selected', 'assert_element_located_to_be_selected'), ('assert_element_located_selection_state_to_be', 'assert_element_located_selection_state_to_be'), ('assert_number_of_windows_to_be', 'assert_number_of_windows_to_be'), ('assert_alert_is_present', 'assert_alert_is_present'), ('assert_text_of_alert', 'assert_text_of_alert')], max_length=255, verbose_name='操作关键字')),
                ('target', models.CharField(blank=True, max_length=255, null=True, verbose_name='操作对象')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='数据项')),
                ('desc', models.CharField(blank=True, max_length=255, verbose_name='操作描述')),
                ('WebCase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebUiAutoTest.webcase', verbose_name='用例前/后置条件')),
            ],
            options={
                'verbose_name': '测试步骤',
                'verbose_name_plural': '测试步骤列表',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='FrontPostStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1, verbose_name='执行顺序')),
                ('command', models.CharField(choices=[('click', '点击'), ('close', '关闭'), ('double_click', '双击'), ('drag_and_drop_to_object', '拖拽到对象'), ('execute_script', '执行脚本'), ('execute_async_script', '执行异步脚本'), ('mouse_over', '鼠标悬停'), ('open', '打开'), ('pause', '等待'), ('select', '选择'), ('select_frame', '选择frame'), ('switch_to_parent_frame', '返回上级frame'), ('select_window', '选择窗口'), ('send_keys', '输入'), ('store', '存储'), ('store_text', '存储文本'), ('store_title', '存储标题'), ('store_value', '存储值'), ('store_xpath_count', '存储xpath总数'), ('add_cookie', '添加cookie'), ('submit', '提交'), ('wait_for_element_not_visible', '等待元素不可见'), ('wait_for_element_present', '待待元素发送'), ('wait_for_element_visible', '等待元素可见'), ('assert_variable', '断言变量'), ('assert_title_is', '断言标题是'), ('assert_title_contains', 'assert_title_包含'), ('assert_url_contains', 'assert_url_包含'), ('assert_url_matches', 'assert_url_匹配'), ('assert_url_to_be', 'assert_url_to_be'), ('assert_url_changes', 'assert_url_变化'), ('assert_presence_of_element_located', 'assert_presence_of_element_located'), ('assert_presence_of_all_elements_located', 'assert_presence_of_all_elements_located'), ('assert_visibility_of_element_located', 'assert_visibility_of_element_located'), ('assert_invisibility_of_element_located', 'assert_invisibility_of_element_located'), ('assert_invisibility_of_element', 'assert_invisibility_of_element'), ('assert_visibility_of', 'assert_visibility_of'), ('assert_visibility_of_any_elements_located', 'assert_visibility_of_any_elements_located'), ('assert_visibility_of_all_elements_located', 'assert_visibility_of_all_elements_located'), ('assert_element_to_be_clickable', 'assert_element_to_be_clickable'), ('assert_staleness_of', 'assert_staleness_of'), ('assert_text_to_be_present_in_element', 'assert_text_to_be_present_in_element'), ('assert_text_to_be_present_in_element_value', 'assert_text_to_be_present_in_element_value'), ('assert_frame_to_be_available_and_switch_to_it', 'assert_frame_to_be_available_and_switch_to_it'), ('assert_element_to_be_selected', 'assert_element_to_be_selected'), ('assert_element_located_to_be_selected', 'assert_element_located_to_be_selected'), ('assert_element_located_selection_state_to_be', 'assert_element_located_selection_state_to_be'), ('assert_number_of_windows_to_be', 'assert_number_of_windows_to_be'), ('assert_alert_is_present', 'assert_alert_is_present'), ('assert_text_of_alert', 'assert_text_of_alert')], max_length=255, verbose_name='操作关键字')),
                ('target', models.CharField(blank=True, max_length=255, null=True, verbose_name='操作对象')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='数据项')),
                ('desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='操作描述')),
                ('FrontPostManager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebUiAutoTest.frontpostmanager', verbose_name='前/后置条件')),
            ],
            options={
                'verbose_name': '前/后置用例',
                'verbose_name_plural': '前/后置用例列表',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='DdtParams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('argvName', models.CharField(max_length=64, verbose_name='参数名')),
                ('argvValue', models.CharField(max_length=1024, verbose_name='参数值')),
                ('DdtData', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebUiAutoTest.ddtdata', verbose_name='数据驱动项')),
            ],
            options={
                'verbose_name': '数据驱动数据项',
                'verbose_name_plural': '数据驱动数据项列表',
            },
        ),
        migrations.AddField(
            model_name='ddtdata',
            name='WebCase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebUiAutoTest.webcase', verbose_name='测试用例'),
        ),
        migrations.CreateModel(
            name='CaseContext',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('argvName', models.CharField(max_length=50, verbose_name='参数名')),
                ('argvValue', models.CharField(max_length=1024, verbose_name='参数值')),
                ('WebCase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebUiAutoTest.webcase', verbose_name='测试用例')),
            ],
            options={
                'verbose_name': '上下文参数定义',
                'verbose_name_plural': '上下文参数定义列表',
            },
        ),
    ]