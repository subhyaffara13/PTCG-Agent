import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run.deps import check_and_install_dependencies
from run.handler import log_crash

sys.excepthook = log_crash


from utils.main import main


if __name__ == "__main__":
    main()
