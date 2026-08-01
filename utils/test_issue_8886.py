
def test_issue_8886():
    from sympy.physics.mechanics import ReferenceFrame as R
    # if something can't be sympified we assume that it
    # doesn't play well with SymPy and disallow the
    # substitution
    v = R('A').x
    raises(SympifyError, lambda: x.subs(x, v))
    raises(SympifyError, lambda: v.subs(v, x))
    assert v.__eq__(x) is False

