
def test_read_withNoFillValue():
    # For a variable with no fill value, reading data with maskandscale=True
    # should return unmasked data
    fname = pjoin(TEST_DATA_PATH, 'example_3_maskedvals.nc')
    with netcdf_file(fname, maskandscale=True) as f:
        vardata = f.variables['var2_noFillval'][:]
        assert_mask_matches(vardata, [False, False, False])
        assert_equal(vardata, [1,2,3])

