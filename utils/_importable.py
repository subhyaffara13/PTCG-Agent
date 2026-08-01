
def _importable(obj, alias='', source=None, enclosing=False, force=True, \
                                              builtin=True, lstrip=True):
    """get an import string (or the source code) for the given object

    This function will attempt to discover the name of the object, or the repr
    of the object, or the source code for the object. To attempt to force
    discovery of the source code, use source=True, to attempt to force the
    use of an import, use source=False; otherwise an import will be sought
    for objects not defined in __main__. The intent is to build a string
    that can be imported from a python file. obj is the object to inspect.
    If alias is provided, then rename the object with the given alias.

    If source=True, use these options:
      If enclosing=True, then also return any enclosing code.
      If force=True, catch (TypeError,IOError) and try to use import hooks.
      If lstrip=True, ensure there is no indentation in the first line of code.

    If source=False, use these options:
      If enclosing=True, get the import for the outermost enclosing callable.
      If force=True, then don't test the import string before returning it.
      If builtin=True, then force an import for builtins where possible.
    """
    if source is None:
        source = True if isfrommain(obj) else False
    if source: # first try to get the source
        try:
            return getsource(obj, alias, enclosing=enclosing, \
                             force=force, lstrip=lstrip, builtin=builtin)
        except Exception: pass
    try:
        if not _isinstance(obj):
            return getimport(obj, alias, enclosing=enclosing, \
                                  verify=(not force), builtin=builtin)
        # first 'get the import', then 'get the instance'
        _import = getimport(obj, enclosing=enclosing, \
                                 verify=(not force), builtin=builtin)
        name = getname(obj, force=True)
        if not name:
            raise AttributeError("object has no atribute '__name__'")
        _alias = "%s = " % alias if alias else ""
        if alias == name: _alias = ""
        return _import+_alias+"%s\n" % name

    except Exception: pass
    if not source: # try getsource, only if it hasn't been tried yet
        try:
            return getsource(obj, alias, enclosing=enclosing, \
                             force=force, lstrip=lstrip, builtin=builtin)
        except Exception: pass
    # get the name (of functions, lambdas, and classes)
    # or hope that obj can be built from the __repr__
    #XXX: what to do about class instances and such?
    obj = getname(obj, force=force)
    # we either have __repr__ or __name__ (or None)
    if not obj or obj.startswith('<'):
        raise AttributeError("object has no atribute '__name__'")
    _alias = '%s = ' % alias if alias else ''
    if alias == obj: _alias = ''
    return _alias+'%s\n' % obj

