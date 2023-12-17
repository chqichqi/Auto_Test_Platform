# Generated by Django 3.2.23 on 2023-12-15 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WebUiAtuoTest', '0011_auto_20231110_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='webcase',
            name='headless',
            field=models.CharField(choices=[('headless', '无头模式'), ('no_headless', '非头模式')], default='headless', max_length=20, verbose_name='浏览器模式'),
        ),
        migrations.AlterField(
            model_name='frontpoststep',
            name='command',
            field=models.CharField(choices=[('open', '打开'), ('send_keys', '输入'), ('clear', '清空'), ('click', '点击'), ('submit', '提交'), ('close', '关闭'), ('double_click', '双击'), ('drag_and_drop_to_object', '拖拽到对象'), ('execute_script', '执行脚本'), ('execute_async_script', '执行异步脚本'), ('mouse_over', '鼠标悬停'), ('mouse_click_hold', '鼠标按下保持'), ('pause', '等待'), ('select', '选择'), ('select_frame', '选择frame'), ('switch_to_parent_frame', '返回上级frame'), ('select_window', '选择窗口'), ('store', '存储对象'), ('store_text', '存储文本'), ('store_title', '存储页面标题'), ('store_value', '存储属性值'), ('store_xpath_count', '存储xpath总数'), ('add_cookie', '添加cookie'), ('wait_for_element_not_visible', '等待元素不可见'), ('wait_for_element_present', '等待元素出现'), ('wait_for_element_visible', '等待元素可见'), ('assert_variable', '断言变量'), ('assert_title_is', '断言标题是'), ('assert_title_contains', 'assert_标题包含'), ('assert_url_contains', 'assert_Url包含'), ('assert_url_matches', 'assert_Url匹配'), ('assert_url_to_be', 'assert_url_to_be'), ('assert_url_changes', 'assert_Url更新'), ('assert_presence_of_element_located', 'assert_presence_of_element_located'), ('assert_presence_of_all_elements_located', 'assert_presence_of_all_elements_located'), ('assert_visibility_of_element_located', 'assert_visibility_of_element_located'), ('assert_invisibility_of_element_located', 'assert_invisibility_of_element_located'), ('assert_invisibility_of_element', 'assert_invisibility_of_element'), ('assert_visibility_of', 'assert_visibility_of'), ('assert_visibility_of_any_elements_located', 'assert_visibility_of_any_elements_located'), ('assert_visibility_of_all_elements_located', 'assert_visibility_of_all_elements_located'), ('assert_element_to_be_clickable', 'assert_element_to_be_clickable'), ('assert_staleness_of', 'assert_staleness_of'), ('assert_text_to_be_present_in_element', 'assert_text_to_be_present_in_element'), ('assert_text_to_be_present_in_element_value', 'assert_text_to_be_present_in_element_value'), ('assert_frame_to_be_available_and_switch_to_it', 'assert_frame_to_be_available_and_switch_to_it'), ('assert_element_to_be_selected', 'assert_element_to_be_selected'), ('assert_element_located_to_be_selected', 'assert_element_located_to_be_selected'), ('assert_element_located_selection_state_to_be', 'assert_element_located_selection_state_to_be'), ('assert_number_of_windows_to_be', 'assert_number_of_windows_to_be'), ('assert_alert_is_present', 'assert_alert_is_present'), ('assert_text_of_alert', 'assert_text_of_alert')], max_length=255, verbose_name='操作关键字'),
        ),
        migrations.AlterField(
            model_name='product',
            name='itemName',
            field=models.CharField(max_length=100, verbose_name='项目名称+版本'),
        ),
        migrations.AlterField(
            model_name='webcase',
            name='Product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebUiAtuoTest.product', verbose_name='所属项目+版本'),
        ),
        migrations.AlterField(
            model_name='webcasestep',
            name='command',
            field=models.CharField(choices=[('open', '打开'), ('send_keys', '输入'), ('clear', '清空'), ('click', '点击'), ('submit', '提交'), ('close', '关闭'), ('double_click', '双击'), ('drag_and_drop_to_object', '拖拽到对象'), ('execute_script', '执行脚本'), ('execute_async_script', '执行异步脚本'), ('mouse_over', '鼠标悬停'), ('mouse_click_hold', '鼠标按下保持'), ('pause', '等待'), ('select', '选择'), ('select_frame', '选择frame'), ('switch_to_parent_frame', '返回上级frame'), ('select_window', '选择窗口'), ('store', '存储对象'), ('store_text', '存储文本'), ('store_title', '存储页面标题'), ('store_value', '存储属性值'), ('store_xpath_count', '存储xpath总数'), ('add_cookie', '添加cookie'), ('wait_for_element_not_visible', '等待元素不可见'), ('wait_for_element_present', '等待元素出现'), ('wait_for_element_visible', '等待元素可见'), ('assert_variable', '断言变量'), ('assert_title_is', '断言标题是'), ('assert_title_contains', 'assert_标题包含'), ('assert_url_contains', 'assert_Url包含'), ('assert_url_matches', 'assert_Url匹配'), ('assert_url_to_be', 'assert_url_to_be'), ('assert_url_changes', 'assert_Url更新'), ('assert_presence_of_element_located', 'assert_presence_of_element_located'), ('assert_presence_of_all_elements_located', 'assert_presence_of_all_elements_located'), ('assert_visibility_of_element_located', 'assert_visibility_of_element_located'), ('assert_invisibility_of_element_located', 'assert_invisibility_of_element_located'), ('assert_invisibility_of_element', 'assert_invisibility_of_element'), ('assert_visibility_of', 'assert_visibility_of'), ('assert_visibility_of_any_elements_located', 'assert_visibility_of_any_elements_located'), ('assert_visibility_of_all_elements_located', 'assert_visibility_of_all_elements_located'), ('assert_element_to_be_clickable', 'assert_element_to_be_clickable'), ('assert_staleness_of', 'assert_staleness_of'), ('assert_text_to_be_present_in_element', 'assert_text_to_be_present_in_element'), ('assert_text_to_be_present_in_element_value', 'assert_text_to_be_present_in_element_value'), ('assert_frame_to_be_available_and_switch_to_it', 'assert_frame_to_be_available_and_switch_to_it'), ('assert_element_to_be_selected', 'assert_element_to_be_selected'), ('assert_element_located_to_be_selected', 'assert_element_located_to_be_selected'), ('assert_element_located_selection_state_to_be', 'assert_element_located_selection_state_to_be'), ('assert_number_of_windows_to_be', 'assert_number_of_windows_to_be'), ('assert_alert_is_present', 'assert_alert_is_present'), ('assert_text_of_alert', 'assert_text_of_alert')], max_length=255, verbose_name='操作关键字'),
        ),
    ]