
def _getimport(head, tail, alias='', verify=True, builtin=False):
    """helper to build a likely import string from head and tail of namespace.
    ('head','tail') are used in the following context: "from head import tail"

    If verify=True, then test the import string before returning it.
    If builtin=True, then force an import for builtins where possible.
    If alias is provided, then rename the object on import.
    """
    # special handling for a few common types
    if tail in ['Ellipsis', 'NotImplemented'] and head in ['types']:
        head = len.__module__
    elif tail in ['None'] and head in ['types']:
        _alias = '%s = ' % alias if alias else ''
        if alias == tail: _alias = ''
        return _alias+'%s\n' % tail
    # we don't need to import from builtins, so return ''
#   elif tail in ['NoneType','int','float','long','complex']: return '' #XXX: ?
    if head in ['builtins','__builtin__']:
        # special cases (NoneType, Ellipsis, ...) #XXX: BuiltinFunctionType
        if tail == 'ellipsis': tail = 'EllipsisType'
        if _intypes(tail): head = 'types'
        elif not builtin:
            _alias = '%s = ' % alias if alias else ''
            if alias == tail: _alias = ''
            return _alias+'%s\n' % tail
        else: pass # handle builtins below
    # get likely import string
    if not head: _str = "import %s" % tail
    else: _str = "from %s import %s" % (head, tail)
    _alias = " as %s\n" % alias if alias else "\n"
    if alias == tail: _alias = "\n"
    _str += _alias
    # FIXME: fails on most decorators, currying, and such...
    #        (could look for magic __wrapped__ or __func__ attr)
    #        (could fix in 'namespace' to check obj for closure)
    if verify and not head.startswith('dill.'):# weird behavior for dill
       #print(_str)
        try: exec(_str) #XXX: check if == obj? (name collision)
        except ImportError: #XXX: better top-down or bottom-up recursion?
            _head = head.rsplit(".",1)[0] #(or get all, then compare == obj?)
            if not _head: raise
            if _head != head:
                _str = _getimport(_head, tail, alias, verify)
    return _str

