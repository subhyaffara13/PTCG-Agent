
def get_self_type(func: CallableType, def_info: TypeInfo) -> Type | None:
    default_self = fill_typevars(def_info)
    if isinstance(get_proper_type(func.ret_type), UninhabitedType):
        return func.ret_type
    elif func.arg_types and func.arg_types[0] != default_self and func.arg_kinds[0] == ARG_POS:
        return func.arg_types[0]
    else:
        return None

