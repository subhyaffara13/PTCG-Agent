
def dispatch_method(self, basename, arg, **options):
    """Dispatch a method to the proper handlers."""
    method_name = '%s_%s' % (basename, arg.__class__.__name__)
    if hasattr(self, method_name):
        f = getattr(self, method_name)
        # This can raise and we will allow it to propagate.
        result = f(arg, **options)
        if result is not None:
            return result
    raise NotImplementedError(
        "%s.%s cannot handle: %r" %
        (self.__class__.__name__, basename, arg)
    )

