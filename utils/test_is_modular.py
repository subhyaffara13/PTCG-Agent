
def test_is_modular():
    assert _is_modular(y, x) is False
    assert _is_modular(Mod(x, 3) - 1, x) is True
    assert _is_modular(Mod(x**3 - 3*x**2 - x + 1, 3) - 1, x) is True
    assert _is_modular(Mod(exp(x + y), 3) - 2, x) is True
    assert _is_modular(Mod(exp(x + y), 3) - log(x), x) is True
    assert _is_modular(Mod(x, 3) - 1, y) is False
    assert _is_modular(Mod(x, 3)**2 - 5, x) is False
    assert _is_modular(Mod(x, 3)**2 - y, x) is False
    assert _is_modular(exp(Mod(x, 3)) - 1, x) is False
    assert _is_modular(Mod(3, y) - 1, y) is False

