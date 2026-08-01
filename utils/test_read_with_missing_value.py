
def test_read_withMissingValue():
    # For a variable with missing_value but not _FillValue, the missing_value
    # should be used
    fname = pjoin(TEST_DATA_PATH, 'example_3_maskedvals.nc')
    with netcdf_file(fname, maskandscale=True) as f:
        vardata = f.variables['var4_missingValue'][:]
        assert_mask_matches(vardata, [False, True, False])

