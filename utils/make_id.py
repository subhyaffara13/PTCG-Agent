
def make_id(obj: object) -> c.Hashable:
    """Get a stable identifier for a receiver or sender, to be used as a dict
    key or in a set.
    """
    if inspect.ismethod(obj):
        # The id of a bound method is not stable, but the id of the unbound
        # function and instance are.
        return id(obj.__func__), id(obj.__self__)

    if isinstance(obj, (str, int)):
        # Instances with the same value always compare equal and have the same
        # hash, even if the id may change.
        return obj

    # Assume other types are not hashable but will always be the same instance.
    return id(obj)

