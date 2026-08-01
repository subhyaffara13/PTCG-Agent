
def apply_skip_if_not_implemented(cls):
    """
    Class decorator to apply @skip_if_not_implemented to all test methods.
    """
    for attr_name in dir(cls):
        if attr_name.startswith("test_"):
            attr = getattr(cls, attr_name)
            if callable(attr):
                setattr(cls, attr_name, skip_if_not_implemented(attr))
    return cls

