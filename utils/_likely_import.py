
def _likely_import(first, last, passive=False, explicit=True):
    return _getimport(first, last, verify=(not passive), builtin=explicit)

