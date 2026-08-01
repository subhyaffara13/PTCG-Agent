
def _load_entry_from_hubconf(m, model):
    if not isinstance(model, str):
        raise ValueError("Invalid input: model should be a string of function name")

    # Note that if a missing dependency is imported at top level of hubconf, it will
    # throw before this function. It's a chicken and egg situation where we have to
    # load hubconf to know what're the dependencies, but to import hubconf it requires
    # a missing package. This is fine, Python will throw proper error message for users.
    _check_dependencies(m)

    func = _load_attr_from_module(m, model)

    if func is None or not callable(func):
        raise RuntimeError(f"Cannot find callable {model} in hubconf")

    return func

