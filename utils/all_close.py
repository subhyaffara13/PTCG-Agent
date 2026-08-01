
def all_close(expr1, expr2, rtol=1e-5, atol=1e-8):
    """Return True if expr1 and expr2 are numerically close.

    The expressions must have the same structure, but any Rational, Integer, or
    Float numbers they contain are compared approximately using rtol and atol.
    Any other parts of expressions are compared exactly. However, allowance is
    made to allow for the additive and multiplicative identities.

    Relative tolerance is measured with respect to expr2 so when used in
    testing expr2 should be the expected correct answer.

    Examples
    ========

    >>> from sympy import exp
    >>> from sympy.abc import x, y
    >>> from sympy.core.numbers import all_close
    >>> expr1 = 0.1*exp(x - y)
    >>> expr2 = exp(x - y)/10
    >>> expr1
    0.1*exp(x - y)
    >>> expr2
    exp(x - y)/10
    >>> expr1 == expr2
    False
    >>> all_close(expr1, expr2)
    True

    Identities are automatically supplied:

    >>> all_close(x, x + 1e-10)
    True
    >>> all_close(x, 1.0*x)
    True
    >>> all_close(x, 1.0*x + 1e-10)
    True

    """
    NUM_TYPES = (Rational, Float)

    def _all_close(obj1, obj2):
        if type(obj1) == type(obj2) and isinstance(obj1, (list, tuple)):
            if len(obj1) != len(obj2):
                return False
            return all(_all_close(e1, e2) for e1, e2 in zip(obj1, obj2))
        else:
            return _all_close_expr(_sympify(obj1), _sympify(obj2))

    def _all_close_expr(expr1, expr2):
        num1 = isinstance(expr1, NUM_TYPES)
        num2 = isinstance(expr2, NUM_TYPES)
        if num1 != num2:
            return False
        elif num1:
            return _close_num(expr1, expr2)
        if expr1.is_Add or expr1.is_Mul or expr2.is_Add or expr2.is_Mul:
            return _all_close_ac(expr1, expr2)
        if expr1.func != expr2.func or len(expr1.args) != len(expr2.args):
            return False
        args = zip(expr1.args, expr2.args)
        return all(_all_close_expr(a1, a2) for a1, a2 in args)

    def _close_num(num1, num2):
        return bool(abs(num1 - num2) <= atol + rtol*abs(num2))

    def _all_close_ac(expr1, expr2):
        # compare expressions with associative commutative operators for
        # approximate equality by seeing that all terms have equivalent
        # coefficients (which are always Rational or Float)
        if expr1.is_Mul or expr2.is_Mul:
            # as_coeff_mul automatically will supply coeff of 1
            c1, e1 = expr1.as_coeff_mul(rational=False)
            c2, e2 = expr2.as_coeff_mul(rational=False)
            if not _close_num(c1, c2):
                return False
            s1 = set(e1)
            s2 = set(e2)
            common = s1 & s2
            s1 -= common
            s2 -= common
            if not s1:
                return True
            if not any(i.has(Float) for j in (s1, s2) for i in j):
                return False
            # factors might not be matching, e.g.
            # x != x**1.0, exp(x) != exp(1.0*x), etc...
            s1 = [i.as_base_exp() for i in ordered(s1)]
            s2 = [i.as_base_exp() for i in ordered(s2)]
            unmatched = list(range(len(s1)))
            for be1 in s1:
                for i in unmatched:
                    be2 = s2[i]
                    if _all_close(be1, be2):
                        unmatched.remove(i)
                        break
                else:
                    return False
            return not(unmatched)
        assert expr1.is_Add or expr2.is_Add
        cd1 = expr1.as_coefficients_dict()
        cd2 = expr2.as_coefficients_dict()
        # this test will assure that the key of 1 is in
        # each dict and that they have equal values
        if not _close_num(cd1[1], cd2[1]):
            return False
        if len(cd1) != len(cd2):
            return False
        for k in list(cd1):
            if k in cd2:
                if not _close_num(cd1.pop(k), cd2.pop(k)):
                    return False
            # k (or a close version in cd2) might have
            # Floats in a factor of the term which will
            # be handled below
        else:
            if not cd1:
                return True
        for k1 in cd1:
            for k2 in cd2:
                if _all_close_expr(k1, k2):
                    # found a matching key
                    # XXX there could be a corner case where
                    # more than 1 might match and the numbers are
                    # such that one is better than the other
                    # that is not being considered here
                    if not _close_num(cd1[k1], cd2[k2]):
                        return False
                    break
            else:
                # no key matched
                return False
        return True

    return _all_close(expr1, expr2)

