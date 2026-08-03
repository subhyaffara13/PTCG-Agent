from typing import Set, Tuple

def _process_limits(*symbols, discrete=None):
    """Process the list of symbols and convert them to canonical limits,
    storing them as Tuple(symbol, lower, upper). The orientation of
    the function is also returned when the upper limit is missing
    so (x, 1, None) becomes (x, None, 1) and the orientation is changed.
    In the case that a limit is specified as (symbol, Range), a list of
    length 4 may be returned if a change of variables is needed; the
    expression that should replace the symbol in the expression is
    the fourth element in the list.
    """
    limits = []
    orientation = 1
    if discrete is None:
        err_msg = 'discrete must be True or False'
    elif discrete:
        err_msg = 'use Range, not Interval or Relational'
    else:
        err_msg = 'use Interval or Relational, not Range'
    for V in symbols:
        if isinstance(V, (Relational, BooleanFunction)):
            if discrete:
                raise TypeError(err_msg)
            variable = V.atoms(Symbol).pop()
            V = (variable, V.as_set())
        elif isinstance(V, Symbol) or getattr(V, '_diff_wrt', False):
            if isinstance(V, Idx):
                if V.lower is None or V.upper is None:
                    limits.append(Tuple(V))
                else:
                    limits.append(Tuple(V, V.lower, V.upper))
            else:
                limits.append(Tuple(V))
            continue
        if is_sequence(V) and not isinstance(V, Set):
            if len(V) == 2 and isinstance(V[1], Set):
                V = list(V)
                if isinstance(V[1], Interval):  # includes Reals
                    if discrete:
                        raise TypeError(err_msg)
                    V[1:] = V[1].inf, V[1].sup
                elif isinstance(V[1], Range):
                    if not discrete:
                        raise TypeError(err_msg)
                    lo = V[1].inf
                    hi = V[1].sup
                    dx = abs(V[1].step)  # direction doesn't matter
                    if dx == 1:
                        V[1:] = [lo, hi]
                    else:
                        if lo is not S.NegativeInfinity:
                            V = [V[0]] + [0, (hi - lo)//dx, dx*V[0] + lo]
                        else:
                            V = [V[0]] + [0, S.Infinity, -dx*V[0] + hi]
                else:
                    # more complicated sets would require splitting, e.g.
                    # Union(Interval(1, 3), interval(6,10))
                    raise NotImplementedError(
                        'expecting Range' if discrete else
                        'Relational or single Interval' )
            V = sympify(flatten(V))  # list of sympified elements/None
            if isinstance(V[0], (Symbol, Idx)) or getattr(V[0], '_diff_wrt', False):
                newsymbol = V[0]
                if len(V) == 3:
                    # general case
                    if V[2] is None and V[1] is not None:
                        orientation *= -1
                    V = [newsymbol] + [i for i in V[1:] if i is not None]

                lenV = len(V)
                if not isinstance(newsymbol, Idx) or lenV == 3:
                    if lenV == 4:
                        limits.append(Tuple(*V))
                        continue
                    if lenV == 3:
                        if isinstance(newsymbol, Idx):
                            # Idx represents an integer which may have
                            # specified values it can take on; if it is
                            # given such a value, an error is raised here
                            # if the summation would try to give it a larger
                            # or smaller value than permitted. None and Symbolic
                            # values will not raise an error.
                            lo, hi = newsymbol.lower, newsymbol.upper
                            try:
                                if lo is not None and not bool(V[1] >= lo):
                                    raise ValueError("Summation will set Idx value too low.")
                            except TypeError:
                                pass
                            try:
                                if hi is not None and not bool(V[2] <= hi):
                                    raise ValueError("Summation will set Idx value too high.")
                            except TypeError:
                                pass
                        limits.append(Tuple(*V))
                        continue
                    if lenV == 1 or (lenV == 2 and V[1] is None):
                        limits.append(Tuple(newsymbol))
                        continue
                    elif lenV == 2:
                        limits.append(Tuple(newsymbol, V[1]))
                        continue

        raise ValueError('Invalid limits given: %s' % str(symbols))

    return limits, orientation


def _process_limits(func, limits):
    """
    Limits should be of the form (x, start, stop).
    x should be a symbol. Both start and stop should be bounded.

    Explanation
    ===========

    * If x is not given, x is determined from func.
    * If limits is None. Limit of the form (x, -pi, pi) is returned.

    Examples
    ========

    >>> from sympy.series.fourier import _process_limits as pari
    >>> from sympy.abc import x
    >>> pari(x**2, (x, -2, 2))
    (x, -2, 2)
    >>> pari(x**2, (-2, 2))
    (x, -2, 2)
    >>> pari(x**2, None)
    (x, -pi, pi)
    """
    def _find_x(func):
        free = func.free_symbols
        if len(free) == 1:
            return free.pop()
        elif not free:
            return Dummy('k')
        else:
            raise ValueError(
                " specify dummy variables for %s. If the function contains"
                " more than one free symbol, a dummy variable should be"
                " supplied explicitly e.g. FourierSeries(m*n**2, (n, -pi, pi))"
                % func)

    x, start, stop = None, None, None
    if limits is None:
        x, start, stop = _find_x(func), -pi, pi
    if is_sequence(limits, Tuple):
        if len(limits) == 3:
            x, start, stop = limits
        elif len(limits) == 2:
            x = _find_x(func)
            start, stop = limits

    if not isinstance(x, Symbol) or start is None or stop is None:
        raise ValueError('Invalid limits given: %s' % str(limits))

    unbounded = [S.NegativeInfinity, S.Infinity]
    if start in unbounded or stop in unbounded:
        raise ValueError("Both the start and end value should be bounded")

    return sympify((x, start, stop))

