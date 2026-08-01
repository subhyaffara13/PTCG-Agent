
def np_random_state(random_state_argument):
    """Decorator to generate a numpy RandomState or Generator instance.

    The decorator processes the argument indicated by `random_state_argument`
    using :func:`nx.utils.create_random_state`.
    The argument value can be a seed (integer), or a `numpy.random.RandomState`
    or `numpy.random.RandomState` instance or (`None` or `numpy.random`).
    The latter two options use the global random number generator for `numpy.random`.

    The returned instance is a `numpy.random.RandomState` or `numpy.random.Generator`.

    Parameters
    ----------
    random_state_argument : string or int
        The name or index of the argument to be converted
        to a `numpy.random.RandomState` instance.

    Returns
    -------
    _random_state : function
        Function whose random_state keyword argument is a RandomState instance.

    Examples
    --------
    Decorate functions like this::

       @np_random_state("seed")
       def random_float(seed=None):
           return seed.rand()


       @np_random_state(0)
       def random_float(rng=None):
           return rng.rand()


       @np_random_state(1)
       def random_array(dims, random_state=1):
           return random_state.rand(*dims)

    See Also
    --------
    py_random_state
    """
    return argmap(create_random_state, random_state_argument)

