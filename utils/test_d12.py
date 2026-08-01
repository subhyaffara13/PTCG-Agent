
def test_D12():
    assert (mpi(-4, 2) * x + mpi(1, 3)) ** 2 == mpi(-8, 16)*x**2 + mpi(-24, 12)*x + mpi(1, 9)

