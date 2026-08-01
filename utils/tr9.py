
def TR9(rv):
    """Sum of ``cos`` or ``sin`` terms as a product of ``cos`` or ``sin``.

    Examples
    ========

    >>> from sympy.simplify.fu import TR9
    >>> from sympy import cos, sin
    >>> TR9(cos(1) + cos(2))
    2*cos(1/2)*cos(3/2)
    >>> TR9(cos(1) + 2*sin(1) + 2*sin(2))
    cos(1) + 4*sin(3/2)*cos(1/2)

    If no change is made by TR9, no re-arrangement of the
    expression will be made. For example, though factoring
    of common term is attempted, if the factored expression
    was not changed, the original expression will be returned:

    >>> TR9(cos(3) + cos(3)*cos(2))
    cos(3) + cos(2)*cos(3)

    """

    def f(rv):
        if not rv.is_Add:
            return rv

        def do(rv, first=True):
            # cos(a)+/-cos(b) can be combined into a product of cosines and
            # sin(a)+/-sin(b) can be combined into a product of cosine and
            # sine.
            #
            # If there are more than two args, the pairs which "work" will
            # have a gcd extractable and the remaining two terms will have
            # the above structure -- all pairs must be checked to find the
            # ones that work. args that don't have a common set of symbols
            # are skipped since this doesn't lead to a simpler formula and
            # also has the arbitrariness of combining, for example, the x
            # and y term instead of the y and z term in something like
            # cos(x) + cos(y) + cos(z).

            if not rv.is_Add:
                return rv

            args = list(ordered(rv.args))
            if len(args) != 2:
                hit = False
                for i in range(len(args)):
                    ai = args[i]
                    if ai is None:
                        continue
                    for j in range(i + 1, len(args)):
                        aj = args[j]
                        if aj is None:
                            continue
                        was = ai + aj
                        new = do(was)
                        if new != was:
                            args[i] = new  # update in place
                            args[j] = None
                            hit = True
                            break  # go to next i
                if hit:
                    rv = Add(*[_f for _f in args if _f])
                    if rv.is_Add:
                        rv = do(rv)

                return rv

            # two-arg Add
            split = trig_split(*args)
            if not split:
                return rv
            gcd, n1, n2, a, b, iscos = split

            # application of rule if possible
            if iscos:
                if n1 == n2:
                    return gcd*n1*2*cos((a + b)/2)*cos((a - b)/2)
                if n1 < 0:
                    a, b = b, a
                return -2*gcd*sin((a + b)/2)*sin((a - b)/2)
            else:
                if n1 == n2:
                    return gcd*n1*2*sin((a + b)/2)*cos((a - b)/2)
                if n1 < 0:
                    a, b = b, a
                return 2*gcd*cos((a + b)/2)*sin((a - b)/2)

        return process_common_addends(rv, do)  # DON'T sift by free symbols

    return bottom_up(rv, f)

