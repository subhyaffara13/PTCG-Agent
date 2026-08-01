
def vt_mapping_size(
    tx: "InstructionTranslator", obj: "VariableTracker"
) -> "VariableTracker":
    # ref: https://github.com/python/cpython/blob/v3.13.3/Objects/abstract.c#L2308-L2330
    T = maybe_get_python_type(obj)
    if type_implements_mp_length(T):
        return obj.mp_length(tx)

    if type_implements_sq_length(T):
        raise_type_error(tx, f"{obj.python_type_name()} is not a mapping")

    raise_type_error(tx, f"object of type {obj.python_type_name()} has no len()")

