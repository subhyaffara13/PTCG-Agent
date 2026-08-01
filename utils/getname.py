
def getname(obj, force=False, fqn=False): #XXX: throw(?) to raise error on fail?
    """get the name of the object. for lambdas, get the name of the pointer """
    if fqn: return '.'.join(_namespace(obj)) #NOTE: returns 'type'
    module = getmodule(obj)
    if not module: # things like "None" and "1"
        if not force: return None #NOTE: returns 'instance' NOT 'type' #FIXME?
        # handle some special cases
        if hasattr(obj, 'dtype') and not obj.shape:
            return getname(obj.__class__) + "(" + repr(obj.tolist()) + ")" 
        return repr(obj)
    try:
        #XXX: 'wrong' for decorators and curried functions ?
        #       if obj.func_closure: ...use logic from getimportable, etc ?
        name = obj.__name__
        if name == '<lambda>':
            return getsource(obj).split('=',1)[0].strip()
        # handle some special cases
        if module.__name__ in ['builtins','__builtin__']:
            if name == 'ellipsis': name = 'EllipsisType'
        return name
    except AttributeError: #XXX: better to just throw AttributeError ?
        if not force: return None
        name = repr(obj)
        if name.startswith('<'): # or name.split('('):
            return None
        return name

