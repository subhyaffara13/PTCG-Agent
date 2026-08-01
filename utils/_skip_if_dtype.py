
def _skip_if_dtype(arg):
    """'array or dtype' polymorphism.

    Return None for np.int8, dtype('float32') or 'f' etc
           arg for np.empty(3) etc
    """
    if isinstance(arg, str):
        return None
    if type(arg) is type:
        return None if issubclass(arg, np.generic) else arg
    else:
        return None if isinstance(arg, np.dtype) else arg

