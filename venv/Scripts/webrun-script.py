#!D:\test-programs\pythonSpace\my_selenium_test\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'SeleniumRunner==0.0.1','console_scripts','webrun'
__requires__ = 'SeleniumRunner==0.0.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('SeleniumRunner==0.0.1', 'console_scripts', 'webrun')()
    )
