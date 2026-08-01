
def test_open_append():
    # open 'w' put one attr
    with in_tempdir():
        filename = 'append_dat.nc'
        f = netcdf_file(filename, 'w')
        f._attributes['Kilroy'] = 'was here'
        f.close()

        # open again in 'a', read the att and a new one
        f = netcdf_file(filename, 'a')
        assert_equal(f._attributes['Kilroy'], b'was here')
        f._attributes['naughty'] = b'Zoot'
        f.close()

        # open yet again in 'r' and check both atts
        f = netcdf_file(filename, 'r')
        assert_equal(f._attributes['Kilroy'], b'was here')
        assert_equal(f._attributes['naughty'], b'Zoot')
        f.close()

