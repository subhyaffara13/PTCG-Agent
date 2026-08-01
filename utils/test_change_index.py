
def test_change_index():
    b, y, c, d, z = symbols('b, y, c, d, z', integer = True)

    assert Product(x, (x, a, b)).change_index(x, x + 1, y) == \
        Product(y - 1, (y, a + 1, b + 1))
    assert Product(x**2, (x, a, b)).change_index(x, x - 1) == \
        Product((x + 1)**2, (x, a - 1, b - 1))
    assert Product(x**2, (x, a, b)).change_index(x, -x, y) == \
        Product((-y)**2, (y, -b, -a))
    assert Product(x, (x, a, b)).change_index(x, -x - 1) == \
        Product(-x - 1, (x, - b - 1, -a - 1))
    assert Product(x*y, (x, a, b), (y, c, d)).change_index(x, x - 1, z) == \
        Product((z + 1)*y, (z, a - 1, b - 1), (y, c, d))


def test_change_index():
    b, v, w = symbols('b, v, w', integer = True)

    assert Sum(x, (x, a, b)).change_index(x, x + 1, y) == \
        Sum(y - 1, (y, a + 1, b + 1))
    assert Sum(x**2, (x, a, b)).change_index( x, x - 1) == \
        Sum((x+1)**2, (x, a - 1, b - 1))
    assert Sum(x**2, (x, a, b)).change_index( x, -x, y) == \
        Sum((-y)**2, (y, -b, -a))
    assert Sum(x, (x, a, b)).change_index( x, -x - 1) == \
        Sum(-x - 1, (x, -b - 1, -a - 1))
    assert Sum(x*y, (x, a, b), (y, c, d)).change_index( x, x - 1, z) == \
        Sum((z + 1)*y, (z, a - 1, b - 1), (y, c, d))
    assert Sum(x, (x, a, b)).change_index( x, x + v) == \
        Sum(-v + x, (x, a + v, b + v))
    assert Sum(x, (x, a, b)).change_index( x, -x - v) == \
        Sum(-v - x, (x, -b - v, -a - v))
    assert Sum(x, (x, a, b)).change_index(x, w*x, v) == \
        Sum(v/w, (v, b*w, a*w))
    raises(ValueError, lambda: Sum(x, (x, a, b)).change_index(x, 2*x))

