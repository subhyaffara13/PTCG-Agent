
def test_decompose():
    assert decompose(x) == {1: x}
    assert decompose(x**2) == {2: x**2}
    assert decompose(x*y) == {2: x*y}
    assert decompose(x + y) == {1: x + y}
    assert decompose(x**2 + y) == {1: y, 2: x**2}
    assert decompose(8*x**2 + 4*y + 7) == {0: 7, 1: 4*y, 2: 8*x**2}
    assert decompose(x**2 + 3*y*x) == {2: x**2 + 3*x*y}
    assert decompose(9*x**2 + y + 4*x + x**3 + y**2*x + 3) ==\
        {0: 3, 1: 4*x + y, 2: 9*x**2, 3: x**3 + x*y**2}

    assert decompose(x, True) == {x}
    assert decompose(x ** 2, True) == {x**2}
    assert decompose(x * y, True) == {x * y}
    assert decompose(x + y, True) == {x, y}
    assert decompose(x ** 2 + y, True) == {y, x ** 2}
    assert decompose(8 * x ** 2 + 4 * y + 7, True) == {7, 4*y, 8*x**2}
    assert decompose(x ** 2 + 3 * y * x, True) == {x ** 2, 3 * x * y}
    assert decompose(9 * x ** 2 + y + 4 * x + x ** 3 + y ** 2 * x + 3, True) == \
           {3, y, 4*x, 9*x**2, x*y**2, x**3}

