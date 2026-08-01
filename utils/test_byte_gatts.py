
def test_byte_gatts():
    # Check that global "string" atts work like they did before py3k
    # unicode and general bytes confusion
    with in_tempdir():
        filename = 'g_byte_atts.nc'
        f = netcdf_file(filename, 'w')
        f._attributes['holy'] = b'grail'
        f._attributes['witch'] = 'floats'
        f.close()
        f = netcdf_file(filename, 'r')
        assert_equal(f._attributes['holy'], b'grail')
        assert_equal(f._attributes['witch'], b'floats')
        f.close()

