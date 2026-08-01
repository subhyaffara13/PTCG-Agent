
def test_mod_inverse():
    assert mod_inverse(3, 11) == 4
    assert mod_inverse(5, 11) == 9
    assert mod_inverse(21124921, 521512) == 7713
    assert mod_inverse(124215421, 5125) == 2981
    assert mod_inverse(214, 12515) == 1579
    assert mod_inverse(5823991, 3299) == 1442
    assert mod_inverse(123, 44) == 39
    assert mod_inverse(2, 5) == 3
    assert mod_inverse(-2, 5) == 2
    assert mod_inverse(2, -5) == -2
    assert mod_inverse(-2, -5) == -3
    assert mod_inverse(-3, -7) == -5
    x = Symbol('x')
    assert S(2).invert(x) == S.Half
    raises(TypeError, lambda: mod_inverse(2, x))
    raises(ValueError, lambda: mod_inverse(2, S.Half))
    raises(ValueError, lambda: mod_inverse(2, cos(1)**2 + sin(1)**2))

