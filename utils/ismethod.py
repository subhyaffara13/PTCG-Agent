
def ismethod(func):
    """Is func a method?
    Note that this has to work as the method is defined but before the class is
    defined.  At this stage methods look like functions.
    """
    if hasattr(inspect, "signature"):
        signature = inspect.signature(func)
        return signature.parameters.get("self", None) is not None
    else:
        spec = inspect.getfullargspec(func)  # type: ignore[union-attr, assignment]
        return spec and spec.args and spec.args[0] == "self"


def ismethod(func):
    """ Is func a method?

    Note that this has to work as the method is defined but before the class is
    defined.  At this stage methods look like functions.
    """
    signature = inspect.signature(func)
    return signature.parameters.get('self', None) is not None


def ismethod(object):
    """Return true if the object is an instance method.

    Instance method objects provide these attributes:
        __doc__         documentation string
        __name__        name with which this method was defined
        im_class        class object in which this method belongs
        im_func         function object containing implementation of method
        im_self         instance to which this method is bound, or None

    """
    return isinstance(object, types.MethodType)

