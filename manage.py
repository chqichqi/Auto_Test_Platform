#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import time
import logging
import sys
from utils.logManager import Log_Manager


def main():
    """Run administrative tasks."""
    create_time = time.strftime('%Y%m%d', time.localtime())
    Log_Manager().config_logging("log/test_django_" + create_time + '.log', logging.INFO, logging.INFO)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_simpleUi.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
