
def _replace(reps):
    """Return a function that can make the replacements, given in
    ``reps``, on a string. The replacements should be given as mapping.

    Examples
    ========

    >>> from sympy.utilities.misc import _replace
    >>> f = _replace(dict(foo='bar', d='t'))
    >>> f('food')
    'bart'
    >>> f = _replace({})
    >>> f('food')
    'food'
    """
    if not reps:
        return lambda x: x
    D = lambda match: reps[match.group(0)]
    pattern = _re.compile("|".join(
        [_re.escape(k) for k, v in reps.items()]), _re.MULTILINE)
    return lambda string: pattern.sub(D, string)

