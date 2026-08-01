
def test_reverse_order():
    x, y, a, b, c, d= symbols('x, y, a, b, c, d', integer = True)

    assert Product(x, (x, 0, 3)).reverse_order(0) == Product(1/x, (x, 4, -1))
    assert Product(x*y, (x, 1, 5), (y, 0, 6)).reverse_order(0, 1) == \
           Product(x*y, (x, 6, 0), (y, 7, -1))
    assert Product(x, (x, 1, 2)).reverse_order(0) == Product(1/x, (x, 3, 0))
    assert Product(x, (x, 1, 3)).reverse_order(0) == Product(1/x, (x, 4, 0))
    assert Product(x, (x, 1, a)).reverse_order(0) == Product(1/x, (x, a + 1, 0))
    assert Product(x, (x, a, 5)).reverse_order(0) == Product(1/x, (x, 6, a - 1))
    assert Product(x, (x, a + 1, a + 5)).reverse_order(0) == \
           Product(1/x, (x, a + 6, a))
    assert Product(x, (x, a + 1, a + 2)).reverse_order(0) == \
           Product(1/x, (x, a + 3, a))
    assert Product(x, (x, a + 1, a + 1)).reverse_order(0) == \
           Product(1/x, (x, a + 2, a))
    assert Product(x, (x, a, b)).reverse_order(0) == Product(1/x, (x, b + 1, a - 1))
    assert Product(x, (x, a, b)).reverse_order(x) == Product(1/x, (x, b + 1, a - 1))
    assert Product(x*y, (x, a, b), (y, 2, 5)).reverse_order(x, 1) == \
           Product(x*y, (x, b + 1, a - 1), (y, 6, 1))
    assert Product(x*y, (x, a, b), (y, 2, 5)).reverse_order(y, x) == \
           Product(x*y, (x, b + 1, a - 1), (y, 6, 1))


def test_reverse_order():
    assert Sum(x, (x, 0, 3)).reverse_order(0) == Sum(-x, (x, 4, -1))
    assert Sum(x*y, (x, 1, 5), (y, 0, 6)).reverse_order(0, 1) == \
           Sum(x*y, (x, 6, 0), (y, 7, -1))
    assert Sum(x, (x, 1, 2)).reverse_order(0) == Sum(-x, (x, 3, 0))
    assert Sum(x, (x, 1, 3)).reverse_order(0) == Sum(-x, (x, 4, 0))
    assert Sum(x, (x, 1, a)).reverse_order(0) == Sum(-x, (x, a + 1, 0))
    assert Sum(x, (x, a, 5)).reverse_order(0) == Sum(-x, (x, 6, a - 1))
    assert Sum(x, (x, a + 1, a + 5)).reverse_order(0) == \
                         Sum(-x, (x, a + 6, a))
    assert Sum(x, (x, a + 1, a + 2)).reverse_order(0) == \
           Sum(-x, (x, a + 3, a))
    assert Sum(x, (x, a + 1, a + 1)).reverse_order(0) == \
           Sum(-x, (x, a + 2, a))
    assert Sum(x, (x, a, b)).reverse_order(0) == Sum(-x, (x, b + 1, a - 1))
    assert Sum(x, (x, a, b)).reverse_order(x) == Sum(-x, (x, b + 1, a - 1))
    assert Sum(x*y, (x, a, b), (y, 2, 5)).reverse_order(x, 1) == \
        Sum(x*y, (x, b + 1, a - 1), (y, 6, 1))
    assert Sum(x*y, (x, a, b), (y, 2, 5)).reverse_order(y, x) == \
        Sum(x*y, (x, b + 1, a - 1), (y, 6, 1))

