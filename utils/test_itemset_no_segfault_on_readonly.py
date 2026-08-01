
def test_itemset_no_segfault_on_readonly():
    # Regression test for ticket #1202.
    # Open the test file in read-only mode.

    filename = pjoin(TEST_DATA_PATH, 'example_1.nc')
    with warnings.catch_warnings():
        message = ("Cannot close a netcdf_file opened with mmap=True, when "
                   "netcdf_variables or arrays referring to its data still exist")
        warnings.filterwarnings("ignore", message, RuntimeWarning)
        with netcdf_file(filename, 'r', mmap=True) as f:
            time_var = f.variables['time']

    # time_var.assignValue(42) should raise a RuntimeError--not seg. fault!
    assert_raises(RuntimeError, time_var.assignValue, 42)

