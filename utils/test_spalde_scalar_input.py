
def test_spalde_scalar_input():
    # Ticket #629
    x = np.linspace(0, 10)
    y = x**3
    tck = splrep(x, y, k=3, t=[5])
    res = spalde(np.float64(1), tck)
    des = np.array([1., 3., 6., 6.])
    assert_almost_equal(res, des)

