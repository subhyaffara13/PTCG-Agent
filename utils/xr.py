
def xr():
    """
    Fixture to import xarray so that the test is skipped when xarray is not installed.
    Use this fixture instead of importing xrray in test files.

    Examples
    --------
    Request the xarray fixture by passing in ``xr`` as an argument to the test ::

        def test_imshow_xarray(xr):

            ds = xr.DataArray(np.random.randn(2, 3))
            im = plt.figure().subplots().imshow(ds)
            np.testing.assert_array_equal(im.get_array(), ds)
    """

    xr = pytest.importorskip('xarray')
    return xr

