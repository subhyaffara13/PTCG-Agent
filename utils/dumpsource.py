
def dumpsource(object, alias='', new=False, enclose=True):
    """'dump to source', where the code includes a pickled object.

    If new=True and object is a class instance, then create a new
    instance using the unpacked class source code. If enclose, then
    create the object inside a function enclosure (thus minimizing
    any global namespace pollution).
    """
    from dill import dumps
    pik = repr(dumps(object))
    code = 'import dill\n'
    if enclose:
        stub = '__this_is_a_stub_variable__' #XXX: *must* be same _enclose.stub
        pre = '%s = ' % stub
        new = False #FIXME: new=True doesn't work with enclose=True
    else:
        stub = alias
        pre = '%s = ' % stub if alias else alias

    # if a 'new' instance is not needed, then just dump and load
    if not new or not _isinstance(object):
        code += pre + 'dill.loads(%s)\n' % pik
    else: #XXX: other cases where source code is needed???
        code += getsource(object.__class__, alias='', lstrip=True, force=True)
        mod = repr(object.__module__) # should have a module (no builtins here)
        code += pre + 'dill.loads(%s.replace(b%s,bytes(__name__,"UTF-8")))\n' % (pik,mod)
       #code += 'del %s' % object.__class__.__name__ #NOTE: kills any existing!

    if enclose:
        # generation of the 'enclosure'
        dummy = '__this_is_a_big_dummy_object__'
        dummy = _enclose(dummy, alias=alias)
        # hack to replace the 'dummy' with the 'real' code
        dummy = dummy.split('\n')
        code = dummy[0]+'\n' + indent(code) + '\n'.join(dummy[-3:])

    return code #XXX: better 'dumpsourcelines', returning list of lines?

