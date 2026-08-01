
def box_index(typ, val, c):
    """
    Convert a native index structure to a Index object.

    If our native index is of a numpy string dtype, we'll cast it to
    object.
    """
    # First build a Numpy array object, then wrap it in a Index
    index = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val)

    res = cgutils.alloca_once_value(c.builder, index.parent)

    # Does parent exist?
    # (it means already boxed once, or Index same as original df.index or df.columns)
    # xref https://github.com/numba/numba/blob/596e8a55334cc46854e3192766e643767bd7c934/numba/core/boxing.py#L593C17-L593C17
    with c.builder.if_else(cgutils.is_not_null(c.builder, index.parent)) as (
        has_parent,
        otherwise,
    ):
        with has_parent:
            c.pyapi.incref(index.parent)
        with otherwise:
            # TODO: preserve the original class for the index
            # Also need preserve the name of the Index
            # class_obj = c.pyapi.unserialize(c.pyapi.serialize_object(typ.pyclass))
            class_obj = c.pyapi.unserialize(c.pyapi.serialize_object(Index))
            array_obj = c.box(typ.as_array, index.data)
            if isinstance(typ.dtype, types.UnicodeCharSeq):
                # We converted to numpy string dtype, convert back
                # to object since _simple_new won't do that for uss
                object_str_obj = c.pyapi.unserialize(c.pyapi.serialize_object("object"))
                array_obj = c.pyapi.call_method(array_obj, "astype", (object_str_obj,))
                c.pyapi.decref(object_str_obj)
            # this is basically Index._simple_new(array_obj, name_obj) in python
            index_obj = c.pyapi.call_method(class_obj, "_simple_new", (array_obj,))
            index.parent = index_obj
            c.builder.store(index_obj, res)

            # Decrefs
            c.pyapi.decref(class_obj)
            c.pyapi.decref(array_obj)
    return c.builder.load(res)

