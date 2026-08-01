
def _instancecheck(cls, other) -> bool:
    wrapped = cls.__wrapped__
    other_cls = other.__class__
    is_instance_of = wrapped is other_cls or issubclass(other_cls, wrapped)
    warnings.warn(
        "%r is deprecated and slated for removal in astroid "
        "2.0, use %r instead" % (cls.__class__.__name__, wrapped.__name__),
        PendingDeprecationWarning,
        stacklevel=2,
    )
    return is_instance_of

