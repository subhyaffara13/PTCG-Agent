
def test_index_of_xarray(xr):
    # separate to allow the rest of the tests to run if no xarray...
    X = np.arange(30).reshape(10, 3)
    x = xr.DataArray(X, dims=["x", "y"])
    Idx, Xnew = cbook.index_of(x)
    np.testing.assert_array_equal(X, Xnew)
    IdxRef = np.arange(10)
    np.testing.assert_array_equal(Idx, IdxRef)

