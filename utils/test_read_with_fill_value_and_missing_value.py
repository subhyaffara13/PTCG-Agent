
def test_read_withFillValueAndMissingValue():
    # For a variable with both _FillValue and missing_value, the _FillValue
    # should be used
    IRRELEVANT_VALUE = 9999
    fname = pjoin(TEST_DATA_PATH, 'example_3_maskedvals.nc')
    with netcdf_file(fname, maskandscale=True) as f:
        vardata = f.variables['var3_fillvalAndMissingValue'][:]
        assert_mask_matches(vardata, [True, False, False])
        assert_equal(vardata, [IRRELEVANT_VALUE, 2, 3])

