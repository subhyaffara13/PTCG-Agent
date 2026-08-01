
def getmodule(object, _filename=None, force=False):
    """get the module of the object"""
    from inspect import getmodule as getmod
    module = getmod(object, _filename)
    if module or not force: return module
    import builtins
    from .source import getname
    name = getname(object, force=True)
    return builtins if name in vars(builtins).keys() else None

