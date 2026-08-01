
def _retrieve_constant(spec: "TreeSpec") -> Any:
    """Given a spec from a pytree registered with register_constant, retrieves the constant"""
    if not _is_constant_holder(spec):
        raise AssertionError("spec does not correspond to a registered constant pytree")
    return tree_unflatten([], spec)

