
def trim(line):
    """Remove everything following comment # characters in line.

    >>> from sympy.physics.quantum.qasm import trim
    >>> trim('nothing happens here')
    'nothing happens here'
    >>> trim('something #happens here')
    'something '
    """
    if '#' not in line:
        return line
    return line.split('#')[0]


def trim(s):
    r"""
    Trim something like a docstring to remove the whitespace that
    is common due to indentation and formatting.

    >>> trim("\n\tfoo = bar\n\t\tbar = baz\n")
    'foo = bar\n\tbar = baz'
    """
    return textwrap.dedent(s).strip()


def trim(a, limits=None, inclusive=(True,True), relative=False, axis=None):
    """
    Trims an array by masking the data outside some given limits.

    Returns a masked version of the input array.

    %s

    Examples
    --------
    >>> from scipy.stats.mstats import trim
    >>> z = [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10]
    >>> print(trim(z,(3,8)))
    [-- -- 3 4 5 6 7 8 -- --]
    >>> print(trim(z,(0.1,0.2),relative=True))
    [-- 2 3 4 5 6 7 8 -- --]

    """  # numpydoc ignore=RT01
    if relative:
        return trimr(a, limits=limits, inclusive=inclusive, axis=axis)
    else:
        return trima(a, limits=limits, inclusive=inclusive)


def trim(x):
    return cheb.chebtrim(x, tol=1e-6)


def trim(x):
    return herm.hermtrim(x, tol=1e-6)


def trim(x):
    return herme.hermetrim(x, tol=1e-6)


def trim(x):
    return lag.lagtrim(x, tol=1e-6)


def trim(x):
    return leg.legtrim(x, tol=1e-6)


def trim(x):
    return poly.polytrim(x, tol=1e-6)


def trim(text: str) -> str:
    """Remove leading and trailing whitespace."""
    return text.strip()

