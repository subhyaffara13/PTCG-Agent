
def test_reorder():
    b, y, c, d, z = symbols('b, y, c, d, z', integer = True)

    assert Product(x*y, (x, a, b), (y, c, d)).reorder((0, 1)) == \
        Product(x*y, (y, c, d), (x, a, b))
    assert Product(x, (x, a, b), (x, c, d)).reorder((0, 1)) == \
        Product(x, (x, c, d), (x, a, b))
    assert Product(x*y + z, (x, a, b), (z, m, n), (y, c, d)).reorder(\
        (2, 0), (0, 1)) == Product(x*y + z, (z, m, n), (y, c, d), (x, a, b))
    assert Product(x*y*z, (x, a, b), (y, c, d), (z, m, n)).reorder(\
        (0, 1), (1, 2), (0, 2)) == \
        Product(x*y*z, (x, a, b), (z, m, n), (y, c, d))
    assert Product(x*y*z, (x, a, b), (y, c, d), (z, m, n)).reorder(\
        (x, y), (y, z), (x, z)) == \
        Product(x*y*z, (x, a, b), (z, m, n), (y, c, d))
    assert Product(x*y, (x, a, b), (y, c, d)).reorder((x, 1)) == \
        Product(x*y, (y, c, d), (x, a, b))
    assert Product(x*y, (x, a, b), (y, c, d)).reorder((y, x)) == \
        Product(x*y, (y, c, d), (x, a, b))


def test_reorder():
    b, y, c, d, z = symbols('b, y, c, d, z', integer = True)

    assert Sum(x*y, (x, a, b), (y, c, d)).reorder((0, 1)) == \
        Sum(x*y, (y, c, d), (x, a, b))
    assert Sum(x, (x, a, b), (x, c, d)).reorder((0, 1)) == \
        Sum(x, (x, c, d), (x, a, b))
    assert Sum(x*y + z, (x, a, b), (z, m, n), (y, c, d)).reorder(\
        (2, 0), (0, 1)) == Sum(x*y + z, (z, m, n), (y, c, d), (x, a, b))
    assert Sum(x*y*z, (x, a, b), (y, c, d), (z, m, n)).reorder(\
        (0, 1), (1, 2), (0, 2)) == Sum(x*y*z, (x, a, b), (z, m, n), (y, c, d))
    assert Sum(x*y*z, (x, a, b), (y, c, d), (z, m, n)).reorder(\
        (x, y), (y, z), (x, z)) == Sum(x*y*z, (x, a, b), (z, m, n), (y, c, d))
    assert Sum(x*y, (x, a, b), (y, c, d)).reorder((x, 1)) == \
        Sum(x*y, (y, c, d), (x, a, b))
    assert Sum(x*y, (x, a, b), (y, c, d)).reorder((y, x)) == \
        Sum(x*y, (y, c, d), (x, a, b))

