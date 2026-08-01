
def test_read_withMaskAndScaleFalse():
    # If a variable has a _FillValue (or missing_value) attribute, but is read
    # with maskandscale set to False, the result should be unmasked
    fname = pjoin(TEST_DATA_PATH, 'example_3_maskedvals.nc')
    # Open file with mmap=False to avoid problems with closing a mmap'ed file
    # when arrays referring to its data still exist:
    with netcdf_file(fname, maskandscale=False, mmap=False) as f:
        vardata = f.variables['var3_fillvalAndMissingValue'][:]
        assert_mask_matches(vardata, [False, False, False])
        assert_equal(vardata, [1, 2, 3])

