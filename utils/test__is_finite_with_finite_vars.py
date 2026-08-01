
def test__is_finite_with_finite_vars():
    f = _is_finite_with_finite_vars
    # issue 12482
    assert all(f(1/x) is None for x in (
        Dummy(), Dummy(real=True), Dummy(complex=True)))
    assert f(1/Dummy(real=False)) is True  # b/c it's finite but not 0

