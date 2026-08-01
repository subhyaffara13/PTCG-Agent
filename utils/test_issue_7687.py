
def test_issue_7687():
    from sympy.core.function import Function
    from sympy.abc import x
    f = Function('f')(x)
    ff = Function('f')(x)
    match_with_cache = ff.matches(f)
    assert isinstance(f, type(ff))
    clear_cache()
    ff = Function('f')(x)
    assert isinstance(f, type(ff))
    assert match_with_cache == ff.matches(f)

