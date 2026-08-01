
def unknown_ptr_type(name, structname=None):
    if structname is None:
        structname = '$$%s' % name
    tp = StructType(structname, None, None, None)
    return NamedPointerType(tp, name)

