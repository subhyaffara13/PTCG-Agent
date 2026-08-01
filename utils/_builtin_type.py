
def _builtin_type(name):
    if name == "ClassType":  # pragma: no cover
        # Backward compat to load pickle files generated with cloudpickle
        # < 1.3 even if loading pickle files from older versions is not
        # officially supported.
        return type
    return getattr(types, name)

