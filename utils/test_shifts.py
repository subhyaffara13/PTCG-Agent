
def test_shifts(shifts, dtype):
    rng = np.random.default_rng(0)
    n, k = 70, 10
    A = rng.random((n, n))
    if shifts is not None and ((shifts < 0) or (k > min(n-1-shifts, n))):
        with pytest.raises(ValueError):
            _svdp(A, k, shifts=shifts, kmax=5*k, irl_mode=True, rng=rng)
    else:
        _svdp(A, k, shifts=shifts, kmax=5*k, irl_mode=True, rng=rng)

