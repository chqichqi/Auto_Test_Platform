import logging
from logging.handlers import TimedRotatingFileHandler
import sys


class Log_Manager:
    @staticmethod
    def config_logging(log_file_name, console_level: int = logging.INFO, file_level: int = logging.DEBUG):
        """
        管理日志数据
        :param log_file_name:
        :param console_level:
        :param file_level:
        :return:

        Value	      Type of interval
            S	   等待1秒切换到一个新日志文件
            M	   等待1分钟切换到一个新日志文件
            H	   等待1小时切换到一个新日志文件
            D	   等待1天切换到一个新日志文件
            W	   等待1星期切换到一个新日志文件 (0=Monday)
        midnight   每天0点切换到新的日志
        """
        formatter = logging.Formatter(u'[%(asctime)s - %(levelname)s - %(funcName)s] --> %(message)s')
        # 创建文件对象
        # file_handler = logging.FileHandler(log_file_name, mode='a', encoding="utf8")
        # 修改：采用每天0时自动换日志文件的方式进行创建文件对象 2023-12-14
        file_handler = TimedRotatingFileHandler(log_file_name, when="midnight", encoding="utf8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(file_level)
        # 创建控制台对象
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(console_level)

        logging.basicConfig(level=min(console_level, file_level), handlers=[file_handler, console_handler])
