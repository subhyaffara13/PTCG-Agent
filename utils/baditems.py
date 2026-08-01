
def baditems(obj, exact=False, safe=False): #XXX: obj=globals() ?
    """get items in object that fail to pickle"""
    if not hasattr(obj,'__iter__'): # is not iterable
        return [j for j in (badobjects(obj,0,exact,safe),) if j is not None]
    obj = obj.values() if getattr(obj,'values',None) else obj
    _obj = [] # can't use a set, as items may be unhashable
    [_obj.append(badobjects(i,0,exact,safe)) for i in obj if i not in _obj]
    return [j for j in _obj if j is not None]

