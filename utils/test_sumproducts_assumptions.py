
def test_sumproducts_assumptions():
    M = Symbol('M', integer=True, positive=True)

    m = Symbol('m', integer=True)
    for func in [Sum, Product]:
        assert func(m, (m, -M, M)).is_positive is None
        assert func(m, (m, -M, M)).is_nonpositive is None
        assert func(m, (m, -M, M)).is_negative is None
        assert func(m, (m, -M, M)).is_nonnegative is None
        assert func(m, (m, -M, M)).is_finite is True

    m = Symbol('m', integer=True, nonnegative=True)
    for func in [Sum, Product]:
        assert func(m, (m, 0, M)).is_positive is None
        assert func(m, (m, 0, M)).is_nonpositive is None
        assert func(m, (m, 0, M)).is_negative is False
        assert func(m, (m, 0, M)).is_nonnegative is True
        assert func(m, (m, 0, M)).is_finite is True

    m = Symbol('m', integer=True, positive=True)
    for func in [Sum, Product]:
        assert func(m, (m, 1, M)).is_positive is True
        assert func(m, (m, 1, M)).is_nonpositive is False
        assert func(m, (m, 1, M)).is_negative is False
        assert func(m, (m, 1, M)).is_nonnegative is True
        assert func(m, (m, 1, M)).is_finite is True

    m = Symbol('m', integer=True, negative=True)
    assert Sum(m, (m, -M, -1)).is_positive is False
    assert Sum(m, (m, -M, -1)).is_nonpositive is True
    assert Sum(m, (m, -M, -1)).is_negative is True
    assert Sum(m, (m, -M, -1)).is_nonnegative is False
    assert Sum(m, (m, -M, -1)).is_finite is True
    assert Product(m, (m, -M, -1)).is_positive is None
    assert Product(m, (m, -M, -1)).is_nonpositive is None
    assert Product(m, (m, -M, -1)).is_negative is None
    assert Product(m, (m, -M, -1)).is_nonnegative is None
    assert Product(m, (m, -M, -1)).is_finite is True

    m = Symbol('m', integer=True, nonpositive=True)
    assert Sum(m, (m, -M, 0)).is_positive is False
    assert Sum(m, (m, -M, 0)).is_nonpositive is True
    assert Sum(m, (m, -M, 0)).is_negative is None
    assert Sum(m, (m, -M, 0)).is_nonnegative is None
    assert Sum(m, (m, -M, 0)).is_finite is True
    assert Product(m, (m, -M, 0)).is_positive is None
    assert Product(m, (m, -M, 0)).is_nonpositive is None
    assert Product(m, (m, -M, 0)).is_negative is None
    assert Product(m, (m, -M, 0)).is_nonnegative is None
    assert Product(m, (m, -M, 0)).is_finite is True

    m = Symbol('m', integer=True)
    assert Sum(2, (m, 0, oo)).is_positive is None
    assert Sum(2, (m, 0, oo)).is_nonpositive is None
    assert Sum(2, (m, 0, oo)).is_negative is None
    assert Sum(2, (m, 0, oo)).is_nonnegative is None
    assert Sum(2, (m, 0, oo)).is_finite is None

    assert Product(2, (m, 0, oo)).is_positive is None
    assert Product(2, (m, 0, oo)).is_nonpositive is None
    assert Product(2, (m, 0, oo)).is_negative is False
    assert Product(2, (m, 0, oo)).is_nonnegative is None
    assert Product(2, (m, 0, oo)).is_finite is None

    assert Product(0, (x, M, M-1)).is_positive is True
    assert Product(0, (x, M, M-1)).is_finite is True

