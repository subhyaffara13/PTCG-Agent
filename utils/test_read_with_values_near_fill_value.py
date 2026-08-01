
def test_read_withValuesNearFillValue():
    # Regression test for ticket #5626
    fname = pjoin(TEST_DATA_PATH, 'example_3_maskedvals.nc')
    with netcdf_file(fname, maskandscale=True) as f:
        vardata = f.variables['var1_fillval0'][:]
        assert_mask_matches(vardata, [False, True, False])

