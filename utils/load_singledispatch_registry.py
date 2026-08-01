
def load_singledispatch_registry(builder: IRBuilder, dispatch_func_obj: Value, line: int) -> Value:
    return builder.builder.get_attr(dispatch_func_obj, "registry", dict_rprimitive, line)

