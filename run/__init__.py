import os
import sys
from run.handler import log_crash
from run.deps import check_and_install_dependencies

sys.excepthook = log_crash
