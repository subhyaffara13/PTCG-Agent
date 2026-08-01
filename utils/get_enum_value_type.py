
def get_enum_value_type(e: type[enum.Enum], loc):
    enum_values: List[enum.Enum] = list(e)
    if not enum_values:
        raise ValueError(f"No enum values defined for: '{e.__class__}'")

    types = {type(v.value) for v in enum_values}
    ir_types = [try_ann_to_type(t, loc) for t in types]

    # If Enum values are of different types, an exception will be raised here.
    # Even though Python supports this case, we chose to not implement it to
    # avoid overcomplicate logic here for a rare use case. Please report a
    # feature request if you find it necessary.
    res = torch._C.unify_type_list(ir_types)
    if not res:
        return AnyType.get()
    return res

