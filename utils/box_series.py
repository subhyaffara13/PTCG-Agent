
def box_series(typ, val, c):
    """
    Convert a native series structure to a Series object.
    """
    series = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val)
    series_const_obj = c.pyapi.unserialize(c.pyapi.serialize_object(Series._from_mgr))
    mgr_const_obj = c.pyapi.unserialize(
        c.pyapi.serialize_object(SingleBlockManager.from_array)
    )
    index_obj = c.box(typ.index, series.index)
    array_obj = c.box(typ.as_array, series.values)
    name_obj = c.box(typ.namety, series.name)
    # This is basically equivalent of
    # pd.Series(data=array_obj, index=index_obj)
    # To improve perf, we will construct the Series from a manager
    # object to avoid checks.
    # We'll also set the name attribute manually to avoid validation
    mgr_obj = c.pyapi.call_function_objargs(
        mgr_const_obj,
        (
            array_obj,
            index_obj,
        ),
    )
    mgr_axes_obj = c.pyapi.object_getattr_string(mgr_obj, "axes")
    # Series._constructor_from_mgr(mgr, axes)
    series_obj = c.pyapi.call_function_objargs(
        series_const_obj, (mgr_obj, mgr_axes_obj)
    )
    c.pyapi.object_setattr_string(series_obj, "_name", name_obj)

    # Decrefs
    c.pyapi.decref(series_const_obj)
    c.pyapi.decref(mgr_axes_obj)
    c.pyapi.decref(mgr_obj)
    c.pyapi.decref(mgr_const_obj)
    c.pyapi.decref(index_obj)
    c.pyapi.decref(array_obj)
    c.pyapi.decref(name_obj)

    return series_obj

