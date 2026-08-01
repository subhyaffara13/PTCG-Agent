
def typeof_iloc(val, c) -> IlocType:
    objtype = typeof_impl(val.obj, c)
    return IlocType(objtype)

