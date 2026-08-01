
def test_ewma_adjust():
    vals = Series(np.zeros(1000))
    vals[5] = 1
    result = vals.ewm(span=100, adjust=False).mean().sum()
    assert np.abs(result - 1) < 1e-2

