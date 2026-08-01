
def get_tensors_from(args, kwargs):
    """ Returns a set of all Tensor objects in the given args and kwargs. """
    return set([arg for arg in args if isinstance(arg, Tensor)] +
               [v for v in kwargs.values() if isinstance(v, Tensor)])

