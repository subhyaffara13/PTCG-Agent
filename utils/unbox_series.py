
def unbox_series(typ, obj, c):
    """
    Convert a Series object to a native structure.
    """
    index_obj = c.pyapi.object_getattr_string(obj, "index")
    values_obj = c.pyapi.object_getattr_string(obj, "values")
    name_obj = c.pyapi.object_getattr_string(obj, "name")

    series = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    series.index = c.unbox(typ.index, index_obj).value
    series.values = c.unbox(typ.values, values_obj).value
    series.name = c.unbox(typ.namety, name_obj).value

    # Decrefs
    c.pyapi.decref(index_obj)
    c.pyapi.decref(values_obj)
    c.pyapi.decref(name_obj)

    return NativeValue(series._getvalue())

