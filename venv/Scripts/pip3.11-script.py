#!D:\test-programs\pythonSpace\django_simpleUi\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pip==23.2.1','console_scripts','pip3.11'
__requires__ = 'pip==23.2.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pip==23.2.1', 'console_scripts', 'pip3.11')()
    )
