
def test_M37():
    assert linsolve([x + y + z - 6, 2*x + y + 2*z - 10, x + 3*y + z - 10 ], x, y, z) == \
        FiniteSet((-z + 4, 2, z))

