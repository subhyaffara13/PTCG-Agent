
def object_from_instance(instance: Instance) -> Instance:
    """Construct the type 'builtins.object' from an instance type."""
    # Use the fact that 'object' is always the last class in the mro.
    res = Instance(instance.type.mro[-1], [])
    return res

