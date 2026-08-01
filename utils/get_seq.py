
def get_seq(obj, cache={str: False, frozenset: False, list: True, set: True,
                        dict: True, tuple: True, type: False,
                        types.ModuleType: False, types.FunctionType: False,
                        types.BuiltinFunctionType: False}):
    """
    Gets all the items in a sequence or return None
    """
    try:
        o_type = obj.__class__
    except AttributeError:
        o_type = type(obj)
    hsattr = hasattr
    if o_type in cache:
        if cache[o_type]:
            if hsattr(obj, "copy"):
                return obj.copy()
            return obj
    elif HAS_NUMPY and o_type in (numpy.ndarray, numpy.ma.core.MaskedConstant):
        if obj.shape and obj.size:
            return obj
        else:
            return []
    elif hsattr(obj, "__contains__") and hsattr(obj, "__iter__") \
       and hsattr(obj, "__len__") and hsattr(o_type, "__contains__") \
       and hsattr(o_type, "__iter__") and hsattr(o_type, "__len__"):
        cache[o_type] = True
        if hsattr(obj, "copy"):
            return obj.copy()
        return obj
    else:
        cache[o_type] = False
        return None

