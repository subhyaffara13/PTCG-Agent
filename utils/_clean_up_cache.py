import os

def _clean_up_cache(module):
    cached = module.__file__.split('.', 1)[0] + '.pyc'
    cached = module.__cached__ if hasattr(module, '__cached__') else cached
    pycache = os.path.join(os.path.dirname(module.__file__), '__pycache__')
    for remove, file in [(os.remove, cached), (os.removedirs, pycache)]:
        with suppress(OSError):
            remove(file)

