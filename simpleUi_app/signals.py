from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import TestReport
import shutil


@receiver(pre_delete, sender=TestReport)
def delete_folder_on_record_delete(sender, instance, **kwargs):
    # 删除记录对应的本地文件夹，其数据为：report/20201105/html/index.html
    folder_path = '.'+str(instance.report_detail).split('/html')[0]    # 取到每份报告保存的日期文件目录
    try:
        shutil.rmtree(folder_path)    # 执行删除对应目录（该目录不论是否为空，均会被执行删除）
    except Exception as e:
        print(f"Error deleting folder: {e}")
