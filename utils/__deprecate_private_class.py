
def __deprecate_private_class(c):
    import warnings

    msg = ('{name} is a private class and may break without warning, '
           'it will be moved and or renamed in future versions.')
    msg = msg.format(name=c.__name__)

    class private_class(c):
        __doc__ = c.__doc__

        def __init__(self, *args, **kwargs):
            warnings.warn(msg, DeprecationWarning)
            super(private_class, self).__init__(*args, **kwargs)

    private_class.__name__ = c.__name__

    return private_class

