
def test_interval_mul():
    assert (
        interval(1, 5) * interval(2, 10) == interval(2, 50)) == (True, True)
    a = interval(-1, 1) * interval(2, 10) == interval(-10, 10)
    assert a == (True, True)

    a = interval(-1, 1) * interval(-5, 3) == interval(-5, 5)
    assert a == (True, True)

    assert (interval(1, 3) * 2 == interval(2, 6)) == (True, True)
    assert (3 * interval(-1, 2) == interval(-3, 6)) == (True, True)

    a = 3 * interval(1, 2, is_valid=False)
    assert a.is_valid is False

    a = 3 * interval(1, 2, is_valid=None)
    assert a.is_valid is None

    a = interval(1, 5, is_valid=False) * interval(1, 2, is_valid=None)
    assert a.is_valid is False


def test_interval_mul():
    assert mpi(-1, 0) * inf == mpi(-inf, 0)
    assert mpi(-1, 0) * -inf == mpi(0, inf)
    assert mpi(0, 1) * inf == mpi(0, inf)
    assert mpi(0, 1) * mpi(0, inf) == mpi(0, inf)
    assert mpi(-1, 1) * inf == mpi(-inf, inf)
    assert mpi(-1, 1) * mpi(0, inf) == mpi(-inf, inf)
    assert mpi(-1, 1) * mpi(-inf, inf) == mpi(-inf, inf)
    assert mpi(-inf, 0) * mpi(0, 1) == mpi(-inf, 0)
    assert mpi(-inf, 0) * mpi(0, 0) * mpi(-inf, 0)
    assert mpi(-inf, 0) * mpi(-inf, inf) == mpi(-inf, inf)
    assert mpi(-5,0)*mpi(-32,28) == mpi(-140,160)
    assert mpi(2,3) * mpi(-1,2) == mpi(-3,6)
    # Should be undefined?
    assert mpi(inf, inf) * 0 == mpi(-inf, inf)
    assert mpi(-inf, -inf) * 0 == mpi(-inf, inf)
    assert mpi(0) * mpi(-inf,2) == mpi(-inf,inf)
    assert mpi(0) * mpi(-2,inf) == mpi(-inf,inf)
    assert mpi(-2,inf) * mpi(0) == mpi(-inf,inf)
    assert mpi(-inf,2) * mpi(0) == mpi(-inf,inf)

