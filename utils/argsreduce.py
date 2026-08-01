
def argsreduce(cond, *args):
    """Clean arguments to:

    1. Ensure all arguments are iterable (arrays of dimension at least one
    2. If cond != True and size > 1, ravel(args[i]) where ravel(condition) is
       True, in 1D.

    Return list of processed arguments.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats._distn_infrastructure import argsreduce
    >>> rng = np.random.default_rng()
    >>> A = rng.random((4, 5))
    >>> B = 2
    >>> C = rng.random((1, 5))
    >>> cond = np.ones(A.shape)
    >>> [A1, B1, C1] = argsreduce(cond, A, B, C)
    >>> A1.shape
    (4, 5)
    >>> B1.shape
    (1,)
    >>> C1.shape
    (1, 5)
    >>> cond[2,:] = 0
    >>> [A1, B1, C1] = argsreduce(cond, A, B, C)
    >>> A1.shape
    (15,)
    >>> B1.shape
    (1,)
    >>> C1.shape
    (15,)

    """
    # some distributions assume arguments are iterable.
    newargs = np.atleast_1d(*args)

    # np.atleast_1d returns an array if only one argument, or a list of arrays
    # if more than one argument.
    if not isinstance(newargs, (list | tuple)):
        newargs = (newargs,)

    if np.all(cond):
        # broadcast arrays with cond
        *newargs, cond = np.broadcast_arrays(*newargs, cond)
        return [arg.ravel() for arg in newargs]

    s = cond.shape
    # np.extract returns flattened arrays, which are not broadcastable together
    # unless they are either the same size or size == 1.
    return [(arg if np.size(arg) == 1
            else np.extract(cond, np.broadcast_to(arg, s)))
            for arg in newargs]

