
def test_matchpy_connector():
    if matchpy is None:
        skip("matchpy not installed")

    from multiset import Multiset
    from matchpy import Pattern, Substitution

    w_ = WildDot("w_")
    w__ = WildPlus("w__")
    w___ = WildStar("w___")

    expr = x + y
    pattern = x + w_
    p, subst = _get_first_match(expr, pattern)
    assert p == Pattern(pattern)
    assert subst == Substitution({'w_': y})

    expr = x + y + z
    pattern = x + w__
    p, subst = _get_first_match(expr, pattern)
    assert p == Pattern(pattern)
    assert subst == Substitution({'w__': Multiset([y, z])})

    expr = x + y + z
    pattern = x + y + z + w___
    p, subst = _get_first_match(expr, pattern)
    assert p == Pattern(pattern)
    assert subst == Substitution({'w___': Multiset()})

