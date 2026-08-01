
def test_interval_pow():
    a = 2**interval(1, 2) == interval(2, 4)
    assert a == (True, True)
    a = interval(1, 2)**interval(1, 2) == interval(1, 4)
    assert a == (True, True)
    a = interval(-1, 1)**interval(0.5, 2)
    assert a.is_valid is None
    a = interval(-2, -1) ** interval(1, 2)
    assert a.is_valid is False
    a = interval(-2, -1) ** (1.0 / 2)
    assert a.is_valid is False
    a = interval(-1, 1)**(1.0 / 2)
    assert a.is_valid is None
    a = interval(-1, 1)**(1.0 / 3) == interval(-1, 1)
    assert a == (True, True)
    a = interval(-1, 1)**2 == interval(0, 1)
    assert a == (True, True)
    a = interval(-1, 1) ** (1.0 / 29) == interval(-1, 1)
    assert a == (True, True)
    a = -2**interval(1, 1) == interval(-2, -2)
    assert a == (True, True)

    a = interval(1, 2, is_valid=False)**2
    assert a.is_valid is False

    a = (-3)**interval(1, 2)
    assert a.is_valid is False
    a = (-4)**interval(0.5, 0.5)
    assert a.is_valid is False
    assert ((-3)**interval(1, 1) == interval(-3, -3)) == (True, True)

    a = interval(8, 64)**(2.0 / 3)
    assert abs(a.start - 4) < 1e-10  # eps
    assert abs(a.end - 16) < 1e-10
    a = interval(-8, 64)**(2.0 / 3)
    assert abs(a.start - 4) < 1e-10  # eps
    assert abs(a.end - 16) < 1e-10


def test_interval_pow():
    assert mpi(3)**2 == mpi(9, 9)
    assert mpi(-3)**2 == mpi(9, 9)
    assert mpi(-3, 1)**2 == mpi(0, 9)
    assert mpi(-3, -1)**2 == mpi(1, 9)
    assert mpi(-3, -1)**3 == mpi(-27, -1)
    assert mpi(-3, 1)**3 == mpi(-27, 1)
    assert mpi(-2, 3)**2 == mpi(0, 9)
    assert mpi(-3, 2)**2 == mpi(0, 9)
    assert mpi(4) ** -1 == mpi(0.25, 0.25)
    assert mpi(-4) ** -1 == mpi(-0.25, -0.25)
    assert mpi(4) ** -2 == mpi(0.0625, 0.0625)
    assert mpi(-4) ** -2 == mpi(0.0625, 0.0625)
    assert mpi(0, 1) ** inf == mpi(0, 1)
    assert mpi(0, 1) ** -inf == mpi(1, inf)
    assert mpi(0, inf) ** inf == mpi(0, inf)
    assert mpi(0, inf) ** -inf == mpi(0, inf)
    assert mpi(1, inf) ** inf == mpi(1, inf)
    assert mpi(1, inf) ** -inf == mpi(0, 1)
    assert mpi(2, 3) ** 1 == mpi(2, 3)
    assert mpi(2, 3) ** 0 == 1
    assert mpi(1,3) ** mpi(2) == mpi(1,9)

