
def test_ticket_701(xp):
    # Test generic filter sizes
    arr = xp.asarray(np.arange(4).reshape(2, 2))
    def func(x):
        return np.min(x)  # NB: np.min not xp.min for callables
    res = ndimage.generic_filter(arr, func, size=(1, 1))
    # The following raises an error unless ticket 701 is fixed
    res2 = ndimage.generic_filter(arr, func, size=1)
    xp_assert_equal(res, res2)

