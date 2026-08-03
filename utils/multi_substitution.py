import itertools

def multi_substitution(*substitutions):
    """
    Take a sequence of pairs specifying substitutions, and create
    a function that performs those substitutions.

    >>> multi_substitution(('foo', 'bar'), ('bar', 'baz'))('foo')
    'baz'
    """
    substitutions = itertools.starmap(substitution, substitutions)
    # compose function applies last function first, so reverse the
    #  substitutions to get the expected order.
    substitutions = reversed(tuple(substitutions))
    return compose(*substitutions)

