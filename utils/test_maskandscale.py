
def test_maskandscale():
    t = np.linspace(20, 30, 15)
    t[3] = 100
    tm = np.ma.masked_greater(t, 99)
    fname = pjoin(TEST_DATA_PATH, 'example_2.nc')
    with netcdf_file(fname, maskandscale=True) as f:
        Temp = f.variables['Temperature']
        assert_equal(Temp.missing_value, 9999)
        assert_equal(Temp.add_offset, 20)
        assert_equal(Temp.scale_factor, np.float32(0.01))
        found = Temp[:].compressed()
        del Temp  # Remove ref to mmap, so file can be closed.
        expected = np.round(tm.compressed(), 2)
        assert_allclose(found, expected)

    with in_tempdir():
        newfname = 'ms.nc'
        f = netcdf_file(newfname, 'w', maskandscale=True)
        f.createDimension('Temperature', len(tm))
        temp = f.createVariable('Temperature', 'i', ('Temperature',))
        temp.missing_value = 9999
        temp.scale_factor = 0.01
        temp.add_offset = 20
        temp[:] = tm
        f.close()

        with netcdf_file(newfname, maskandscale=True) as f:
            Temp = f.variables['Temperature']
            assert_equal(Temp.missing_value, 9999)
            assert_equal(Temp.add_offset, 20)
            assert_equal(Temp.scale_factor, np.float32(0.01))
            expected = np.round(tm.compressed(), 2)
            found = Temp[:].compressed()
            del Temp
            assert_allclose(found, expected)

