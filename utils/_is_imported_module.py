import sys

def _is_imported_module(module):
    return getattr(module, '__loader__', None) is not None or module in sys.modules.values()

