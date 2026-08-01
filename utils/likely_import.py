
def likely_import(obj, passive=False, explicit=False):
    return getimport(obj, verify=(not passive), builtin=explicit)

