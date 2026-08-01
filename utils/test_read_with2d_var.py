
def test_read_with2dVar():
    fname = pjoin(TEST_DATA_PATH, 'example_3_maskedvals.nc')
    with netcdf_file(fname, maskandscale=True) as f:
        vardata = f.variables['var7_2d'][:]
        assert_mask_matches(vardata, [[True, False], [False, False], [False, True]])

