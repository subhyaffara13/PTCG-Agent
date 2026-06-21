# conftest.py at root to ensure sys.path includes the root directory
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
