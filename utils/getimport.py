
def getimport(obj, alias='', verify=True, builtin=False, enclosing=False):
    """get the likely import string for the given object

    obj is the object to inspect
    If verify=True, then test the import string before returning it.
    If builtin=True, then force an import for builtins where possible.
    If enclosing=True, get the import for the outermost enclosing callable.
    If alias is provided, then rename the object on import.
    """
    if enclosing:
        from .detect import outermost
        _obj = outermost(obj)
        obj = _obj if _obj else obj
    # get the namespace
    qual = _namespace(obj)
    head = '.'.join(qual[:-1])
    tail = qual[-1]
    # for named things... with a nice repr #XXX: move into _namespace?
    try: # look for '<...>' and be mindful it might be in lists, dicts, etc...
        name = repr(obj).split('<',1)[1].split('>',1)[1]
        name = None # we have a 'object'-style repr
    except Exception: # it's probably something 'importable'
        if head in ['builtins','__builtin__']:
            name = repr(obj) #XXX: catch [1,2], (1,2), set([1,2])... others?
        elif _isinstance(obj):
            name = getname(obj, force=True).split('(')[0]
        else:
            name = repr(obj).split('(')[0]
   #if not repr(obj).startswith('<'): name = repr(obj).split('(')[0]
   #else: name = None
    if name: # try using name instead of tail
        try: return _getimport(head, name, alias, verify, builtin)
        except ImportError: pass
        except SyntaxError:
            if head in ['builtins','__builtin__']:
                _alias = '%s = ' % alias if alias else ''
                if alias == name: _alias = ''
                return _alias+'%s\n' % name
            else: pass
    try:
       #if type(obj) is type(abs): _builtin = builtin # BuiltinFunctionType
       #else: _builtin = False
        return _getimport(head, tail, alias, verify, builtin)
    except ImportError:
        raise # could do some checking against obj
    except SyntaxError:
        if head in ['builtins','__builtin__']:
            _alias = '%s = ' % alias if alias else ''
            if alias == tail: _alias = ''
            return _alias+'%s\n' % tail
        raise # could do some checking against obj

