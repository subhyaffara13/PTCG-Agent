
def test_read_example_data():
    # read any example data files
    for fname in glob(pjoin(TEST_DATA_PATH, '*.nc')):
        with netcdf_file(fname, 'r'):
            pass
        with netcdf_file(fname, 'r', mmap=False):
            pass

