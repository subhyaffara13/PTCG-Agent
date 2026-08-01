
def test_read_write_sio():
    eg_sio1 = BytesIO()
    with make_simple(eg_sio1, 'w'):
        str_val = eg_sio1.getvalue()

    eg_sio2 = BytesIO(str_val)
    with netcdf_file(eg_sio2) as f2:
        check_simple(f2)

    # Test that error is raised if attempting mmap for sio
    eg_sio3 = BytesIO(str_val)
    assert_raises(ValueError, netcdf_file, eg_sio3, 'r', True)
    # Test 64-bit offset write / read
    eg_sio_64 = BytesIO()
    with make_simple(eg_sio_64, 'w', version=2) as f_64:
        str_val = eg_sio_64.getvalue()

    eg_sio_64 = BytesIO(str_val)
    with netcdf_file(eg_sio_64) as f_64:
        check_simple(f_64)
        assert_equal(f_64.version_byte, 2)
    # also when version 2 explicitly specified
    eg_sio_64 = BytesIO(str_val)
    with netcdf_file(eg_sio_64, version=2) as f_64:
        check_simple(f_64)
        assert_equal(f_64.version_byte, 2)

