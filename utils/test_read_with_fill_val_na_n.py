
def test_read_withFillValNaN():
    fname = pjoin(TEST_DATA_PATH, 'example_3_maskedvals.nc')
    with netcdf_file(fname, maskandscale=True) as f:
        vardata = f.variables['var5_fillvalNaN'][:]
        assert_mask_matches(vardata, [False, True, False])

