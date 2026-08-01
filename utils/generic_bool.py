
def generic_bool(tx: "InstructionTranslator", obj: VariableTracker) -> VariableTracker:
    """Mirrors PyObject_IsTrue.

    https://github.com/python/cpython/blob/c09ccd9c429/Objects/object.c#L2135-L2158

    Resolution order: constants → nb_bool → mp_length/sq_length → truthy.
    """
    from .constant import ConstantVariable

    if obj.is_python_constant():
        return ConstantVariable.create(bool(obj.as_python_constant()))

    obj_type = maybe_get_python_type(obj)

    if type_implements_nb_bool(obj_type):
        result = obj.bool_impl(tx)
        if result is not None:
            return result

    try:
        length = generic_len(tx, obj)
        from .tensor import SymNodeVariable

        if isinstance(length, SymNodeVariable):
            return SymNodeVariable.create(tx, length.as_proxy() > 0)
        return ConstantVariable.create(length.as_python_constant() > 0)
    except ObservedTypeError:
        handle_observed_exception(tx)

    return ConstantVariable.create(True)

