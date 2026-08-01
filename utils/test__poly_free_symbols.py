
def test_Poly_free_symbols():
    assert Poly(x**2 + 1).free_symbols == {x}
    assert Poly(x**2 + y*z).free_symbols == {x, y, z}
    assert Poly(x**2 + y*z, x).free_symbols == {x, y, z}
    assert Poly(x**2 + sin(y*z)).free_symbols == {x, y, z}
    assert Poly(x**2 + sin(y*z), x).free_symbols == {x, y, z}
    assert Poly(x**2 + sin(y*z), x, domain=EX).free_symbols == {x, y, z}
    assert Poly(1 + x + x**2, x, y, z).free_symbols == {x}
    assert Poly(x + sin(y), z).free_symbols == {x, y}

