
def importable(obj, alias='', source=None, builtin=True):
    """get an importable string (i.e. source code or the import string)
    for the given object, including any required objects from the enclosing
    and global scope

    This function will attempt to discover the name of the object, or the repr
    of the object, or the source code for the object. To attempt to force
    discovery of the source code, use source=True, to attempt to force the
    use of an import, use source=False; otherwise an import will be sought
    for objects not defined in __main__. The intent is to build a string
    that can be imported from a python file.

    obj is the object to inspect. If alias is provided, then rename the
    object with the given alias. If builtin=True, then force an import for
    builtins where possible.
    """
    #NOTE: we always 'force', and 'lstrip' as necessary
    #NOTE: for 'enclosing', use importable(outermost(obj))
    if source is None:
        source = True if isfrommain(obj) else False
    elif builtin and isbuiltin(obj):
        source = False
    tried_source = tried_import = False
    while True:
        if not source: # we want an import
            try:
                if _isinstance(obj): # for instances, punt to _importable
                    return _importable(obj, alias, source=False, builtin=builtin)
                src = _closuredimport(obj, alias=alias, builtin=builtin)
                if len(src) == 0:
                    raise NotImplementedError('not implemented')
                if len(src) > 1:
                    raise NotImplementedError('not implemented')
                return list(src.values())[0]
            except Exception:
                if tried_source: raise
                tried_import = True
        # we want the source
        try:
            src = _closuredsource(obj, alias=alias)
            if len(src) == 0:
                raise NotImplementedError('not implemented')
            # groan... an inline code stitcher
            def _code_stitcher(block):
                "stitch together the strings in tuple 'block'"
                if block[0] and block[-1]: block = '\n'.join(block)
                elif block[0]: block = block[0]
                elif block[-1]: block = block[-1]
                else: block = ''
                return block
            # get free_vars first
            _src = _code_stitcher(src.pop(None))
            _src = [_src] if _src else []
            # get func_vars
            for xxx in src.values():
                xxx = _code_stitcher(xxx)
                if xxx: _src.append(xxx)
            # make a single source string
            if not len(_src):
                src = ''
            elif len(_src) == 1:
                src = _src[0]
            else:
                src = '\n'.join(_src)
            # get source code of objects referred to by obj in global scope
            from .detect import globalvars
            obj = globalvars(obj) #XXX: don't worry about alias? recurse? etc?
            obj = list(getsource(_obj,name,force=True) for (name,_obj) in obj.items() if not isbuiltin(_obj))
            obj = '\n'.join(obj) if obj else ''
            # combine all referred-to source (global then enclosing)
            if not obj: return src
            if not src: return obj
            return obj + src
        except Exception:
            if tried_import: raise
            tried_source = True
            source = not source
    # should never get here
    return

