
def getimportable(obj, alias='', byname=True, explicit=False):
    return importable(obj,alias,source=(not byname),builtin=explicit)

