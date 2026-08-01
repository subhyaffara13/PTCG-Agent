
def test_mmaps_segfault():
    filename = pjoin(TEST_DATA_PATH, 'example_1.nc')

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        with netcdf_file(filename, mmap=True) as f:
            x = f.variables['lat'][:]
            # should not raise warnings
            del x

    def doit():
        with netcdf_file(filename, mmap=True) as f:
            return f.variables['lat'][:]

    # should not crash
    with warnings.catch_warnings():
        message = ("Cannot close a netcdf_file opened with mmap=True, when "
                   "netcdf_variables or arrays referring to its data still exist")
        warnings.filterwarnings("ignore", message, RuntimeWarning)
        x = doit()
    x.sum()

