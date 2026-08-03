import os
import sys

def color_enabled():
    COLOR_ENV = os.getenv('COLOR', 'auto')
    if COLOR_ENV == 'auto' and sys.stdout.isatty():
        return True
    if COLOR_ENV == 'yes':
        return True
    return False

