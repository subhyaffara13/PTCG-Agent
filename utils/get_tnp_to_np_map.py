
def get_tnp_to_np_map() -> dict[types.FunctionType, types.BuiltinFunctionType]:
    """
    This is just the reverse mapping of get_np_to_tnp_map() - mapping from
    torch._numpy modules to numpy equivalents.
    """
    m = get_np_to_tnp_map()
    return {v: k for k, v in m.items()}

