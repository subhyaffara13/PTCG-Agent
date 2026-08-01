
def _find_custom_op(qualname, also_check_torch_library=False):
    if qualname in global_registry:
        return global_registry[qualname]
    if not also_check_torch_library:
        raise RuntimeError(
            f'Could not find custom op "{qualname}". Did you register it via '
            f"the torch._custom_ops API?"
        )
    overload = get_op(qualname)
    result = custom_op_from_existing(overload)
    return result

