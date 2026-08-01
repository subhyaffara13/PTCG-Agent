
def _gridnd(val_f, c, *args):
    """
    Helper function used to implement the ``<type>grid<n>d`` functions.

    Parameters
    ----------
    val_f : function(array_like, array_like, tensor: bool) -> array_like
        The ``<type>val`` function, such as ``polyval``
    c, args
        See the ``<type>grid<n>d`` functions for more detail
    """
    for xi in args:
        c = val_f(xi, c)
    return c

