
def test_precision():
    f1 = Float("1.01")
    f2 = Float("1.0000000000000000000001")
    for u in [1, 1e-2, 1e-6, 1e-13, 1e-14, 1e-16, 1e-20, 1e-100, 1e-300,
            f1, f2]:
        result = construct_domain([u])
        v = float(result[1][0])
        assert abs(u - v) / u < 1e-14  # Test relative accuracy

    result = construct_domain([f1])
    y = result[1][0]
    assert y-1 > 1e-50

    result = construct_domain([f2])
    y = result[1][0]
    assert y-1 > 1e-50


def test_precision():
    A = randmatrix(10, 10)
    assert mnorm(inverse(inverse(A)) - A, 1) < 1.e-45

