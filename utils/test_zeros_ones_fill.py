
def test_zeros_ones_fill():
    n, m = 3, 5

    a = zeros(n, m)
    a.fill( 5 )

    b = 5 * ones(n, m)

    assert a == b
    assert a.rows == b.rows == 3
    assert a.cols == b.cols == 5
    assert a.shape == b.shape == (3, 5)
    assert zeros(2) == zeros(2, 2)
    assert ones(2) == ones(2, 2)
    assert zeros(2, 3) == Matrix(2, 3, [0]*6)
    assert ones(2, 3) == Matrix(2, 3, [1]*6)

    a.fill(0)
    assert a == zeros(n, m)


def test_zeros_ones_fill():
    n, m = 3, 5

    a = zeros(n, m)
    a.fill( 5 )

    b = 5 * ones(n, m)

    assert a == b
    assert a.rows == b.rows == 3
    assert a.cols == b.cols == 5
    assert a.shape == b.shape == (3, 5)
    assert zeros(2) == zeros(2, 2)
    assert ones(2) == ones(2, 2)
    assert zeros(2, 3) == Matrix(2, 3, [0]*6)
    assert ones(2, 3) == Matrix(2, 3, [1]*6)

    a.fill(0)
    assert a == zeros(n, m)

