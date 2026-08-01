
def unbox_index(typ, obj, c):
    """
    Convert a Index object to a native structure.

    Note: Object dtype is not allowed here
    """
    data_obj = c.pyapi.object_getattr_string(obj, "_numba_data")
    index = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    # If we see an object array, assume its been validated as only containing strings
    # We still need to do the conversion though
    index.data = c.unbox(typ.as_array, data_obj).value
    typed_dict_obj = c.pyapi.unserialize(c.pyapi.serialize_object(numba.typed.Dict))
    # Create an empty typed dict in numba for the hashmap for indexing
    # equiv of numba.typed.Dict.empty(typ.dtype, types.intp)
    arr_type_obj = c.pyapi.unserialize(c.pyapi.serialize_object(typ.dtype))
    intp_type_obj = c.pyapi.unserialize(c.pyapi.serialize_object(types.intp))
    hashmap_obj = c.pyapi.call_method(
        typed_dict_obj, "empty", (arr_type_obj, intp_type_obj)
    )
    index.hashmap = c.unbox(types.DictType(typ.dtype, types.intp), hashmap_obj).value
    # Set the parent for speedy boxing.
    index.parent = obj

    # Decrefs
    c.pyapi.decref(data_obj)
    c.pyapi.decref(arr_type_obj)
    c.pyapi.decref(intp_type_obj)
    c.pyapi.decref(typed_dict_obj)

    return NativeValue(index._getvalue())

