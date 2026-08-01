
def _get_checker() -> doctest.OutputChecker:
    """Return a doctest.OutputChecker subclass that supports some
    additional options:

    * ALLOW_UNICODE and ALLOW_BYTES options to ignore u'' and b''
      prefixes (respectively) in string literals. Useful when the same
      doctest should run in Python 2 and Python 3.

    * NUMBER to ignore floating-point differences smaller than the
      precision of the literal number in the doctest.

    An inner class is used to avoid importing "doctest" at the module
    level.
    """
    global CHECKER_CLASS
    if CHECKER_CLASS is None:
        CHECKER_CLASS = _init_checker_class()
    return CHECKER_CLASS()

