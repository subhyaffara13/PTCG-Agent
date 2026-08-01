
def _picklable_class_constructor(mixin_class, fmt, attr_name, base_class):
    """Internal helper for _make_class_factory."""
    factory = _make_class_factory(mixin_class, fmt, attr_name)
    cls = factory(base_class)
    return cls.__new__(cls)

