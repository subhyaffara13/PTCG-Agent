import re

def _eval_is_eq(lhs, rhs):
    if lhs._size != rhs._size:
        return None
    return lhs._array_form == rhs._array_form


def _eval_is_eq(a, b): # noqa:F811
    return False


def _eval_is_eq(self, other): # noqa: F811
    return False


def _eval_is_eq(lhs, rhs):
    return None


def _eval_is_eq(lhs, rhs):  # noqa:F811
    return False


def _eval_is_eq(lhs, rhs):  # noqa:F811
    return None


def _eval_is_eq(lhs, rhs):  # noqa:F811
    return None


def _eval_is_eq(lhs, rhs):  # noqa:F811
    if len(lhs) != len(rhs):
        return False

    return fuzzy_and(fuzzy_bool(is_eq(s, o)) for s, o in zip(lhs, rhs))


def _eval_is_eq(lhs, rhs): # noqa:F811
    """Helper method for Equality with matrices.sympy.

    Relational automatically converts matrices to ImmutableDenseMatrix
    instances, so this method only applies here.  Returns True if the
    matrices are definitively the same, False if they are definitively
    different, and None if undetermined (e.g. if they contain Symbols).
    Returning None triggers default handling of Equalities.

    """
    if lhs.shape != rhs.shape:
        return False
    return (lhs - rhs).is_zero_matrix


def _eval_is_eq(lhs, rhs): # noqa:F811
    # if we use is_eq to check here, we get infinite recursion
    return lhs == rhs


def _eval_is_eq(lhs, rhs): # noqa:F811
    # CRootOf represents a Root, so if rhs is that root, it should set
    # the expression to zero *and* it should be in the interval of the
    # CRootOf instance. It must also be a number that agrees with the
    # is_real value of the CRootOf instance.
    if not rhs.is_number:
        return None
    if not rhs.is_finite:
        return False
    z = lhs.expr.subs(lhs.expr.free_symbols.pop(), rhs).is_zero
    if z is False:  # all roots will make z True but we don't know
        # whether this is the right root if z is True
        return False
    o = rhs.is_real, rhs.is_imaginary
    s = lhs.is_real, lhs.is_imaginary
    assert None not in s  # this is part of initial refinement
    if o != s and None not in o:
        return False
    re, im = rhs.as_real_imag()
    if lhs.is_real:
        if im:
            return False
        i = lhs._get_interval()
        a, b = [Rational(str(_)) for _ in (i.a, i.b)]
        return sympify(a <= rhs and rhs <= b)
    i = lhs._get_interval()
    r1, r2, i1, i2 = [Rational(str(j)) for j in (
        i.ax, i.bx, i.ay, i.by)]
    return is_le(r1, re) and is_le(re,r2) and is_le(i1,im) and is_le(im,i2)


def _eval_is_eq(lhs, rhs): # noqa: F811
    return False


def _eval_is_eq(lhs, rhs): # noqa: F811
    return False


def _eval_is_eq(lhs, rhs): # noqa: F811
    return And(Eq(lhs.left, rhs.left),
               Eq(lhs.right, rhs.right),
               lhs.left_open == rhs.left_open,
               lhs.right_open == rhs.right_open)


def _eval_is_eq(lhs, rhs): # noqa: F811
    def all_in_both():
        s_set = set(lhs.args)
        o_set = set(rhs.args)
        yield fuzzy_and(lhs._contains(e) for e in o_set - s_set)
        yield fuzzy_and(rhs._contains(e) for e in s_set - o_set)

    return tfn[fuzzy_and(all_in_both())]


def _eval_is_eq(lhs, rhs): # noqa: F811
    if len(lhs.sets) != len(rhs.sets):
        return False

    eqs = (is_eq(x, y) for x, y in zip(lhs.sets, rhs.sets))
    return tfn[fuzzy_and(map(fuzzy_bool, eqs))]


def _eval_is_eq(lhs, rhs): # noqa: F811
    return False


def _eval_is_eq(lhs, rhs): # noqa: F811
    return tfn[fuzzy_and(a.is_subset(b) for a, b in [(lhs, rhs), (rhs, lhs)])]


def _eval_is_eq(lhs, rhs): # noqa:F811
    return False


def _eval_is_eq(lhs, rhs): # noqa:F811
    if lhs.shape != rhs.shape:
        return False
    if (lhs - rhs).is_ZeroMatrix:
        return True


def _eval_is_eq(lhs, rhs): # noqa:F811
    return is_eq(lhs.rewrite(ceiling), rhs) or \
        is_eq(lhs.rewrite(frac),rhs)


def _eval_is_eq(lhs, rhs): # noqa:F811
    return is_eq(lhs.rewrite(floor), rhs) or is_eq(lhs.rewrite(frac),rhs)


def _eval_is_eq(lhs, rhs): # noqa:F811
    if (lhs.rewrite(floor) == rhs) or \
        (lhs.rewrite(ceiling) == rhs):
        return True
    # Check if other < 0
    if rhs.is_extended_negative:
        return False
    # Check if other >= 1
    res = lhs._value_one_or_more(rhs)
    if res is not None:
        return False

