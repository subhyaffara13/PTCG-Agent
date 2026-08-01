
def create_py_random_state(random_state=None):
    """Returns a random.Random instance depending on input.

    Parameters
    ----------
    random_state : int or random number generator or None (default=None)
        - If int, return a `random.Random` instance set with seed=int.
        - If `random.Random` instance, return it.
        - If None or the `np.random` package, return the global random number
          generator used by `np.random`.
        - If an `np.random.Generator` instance, or the `np.random` package, or
          the global numpy random number generator, then return it.
          wrapped in a `PythonRandomViaNumpyBits` class.
        - If a `PythonRandomViaNumpyBits` instance, return it.
        - If a `PythonRandomInterface` instance, return it.
        - If a `np.random.RandomState` instance and not the global numpy default,
          return it wrapped in `PythonRandomInterface` for backward bit-stream
          matching with legacy code.

    Notes
    -----
    - A diagram intending to illustrate the relationships behind our support
      for numpy random numbers is called
      `NetworkX Numpy Random Numbers <https://excalidraw.com/#room=b5303f2b03d3af7ccc6a,e5ZDIWdWWCTTsg8OqoRvPA>`_.
    - More discussion about this support also appears in
      `gh-6869#comment <https://github.com/networkx/networkx/pull/6869#issuecomment-1944799534>`_.
    - Wrappers of numpy.random number generators allow them to mimic the Python random
      number generation algorithms. For example, Python can create arbitrarily large
      random ints, and the wrappers use Numpy bit-streams with CPython's random module
      to choose arbitrarily large random integers too.
    - We provide two wrapper classes:
      `PythonRandomViaNumpyBits` is usually what you want and is always used for
      `np.Generator` instances. But for users who need to recreate random numbers
      produced in NetworkX 3.2 or earlier, we maintain the `PythonRandomInterface`
      wrapper as well. We use it only used if passed a (non-default) `np.RandomState`
      instance pre-initialized from a seed. Otherwise the newer wrapper is used.
    """
    if random_state is None or random_state is random:
        return random._inst
    if isinstance(random_state, random.Random):
        return random_state
    if isinstance(random_state, int):
        return random.Random(random_state)

    try:
        import numpy as np
    except ImportError:
        pass
    else:
        if isinstance(random_state, PythonRandomInterface | PythonRandomViaNumpyBits):
            return random_state
        if isinstance(random_state, np.random.Generator):
            return PythonRandomViaNumpyBits(random_state)
        if random_state is np.random:
            return PythonRandomViaNumpyBits(np.random.mtrand._rand)

        if isinstance(random_state, np.random.RandomState):
            if random_state is np.random.mtrand._rand:
                return PythonRandomViaNumpyBits(random_state)
            # Only need older interface if specially constructed RandomState used
            return PythonRandomInterface(random_state)

    msg = f"{random_state} cannot be used to generate a random.Random instance"
    raise ValueError(msg)

