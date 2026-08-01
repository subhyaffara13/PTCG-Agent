
def test_PurePoly_free_symbols():
    assert PurePoly(x**2 + 1).free_symbols == set()
    assert PurePoly(x**2 + y*z).free_symbols == set()
    assert PurePoly(x**2 + y*z, x).free_symbols == {y, z}
    assert PurePoly(x**2 + sin(y*z)).free_symbols == set()
    assert PurePoly(x**2 + sin(y*z), x).free_symbols == {y, z}
    assert PurePoly(x**2 + sin(y*z), x, domain=EX).free_symbols == {y, z}

