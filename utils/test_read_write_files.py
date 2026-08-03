import os

def test_read_write_files():
    # test round trip for example file
    cwd = os.getcwd()
    try:
        tmpdir = tempfile.mkdtemp()
        os.chdir(tmpdir)
        with make_simple('simple.nc', 'w') as f:
            pass
        # read the file we just created in 'a' mode
        with netcdf_file('simple.nc', 'a') as f:
            check_simple(f)
            # add something
            f._attributes['appendRan'] = 1

        # To read the NetCDF file we just created::
        with netcdf_file('simple.nc') as f:
            # Using mmap is the default
            assert f.use_mmap
            check_simple(f)
            assert_equal(f._attributes['appendRan'], 1)

        # Read it in append (and check mmap is off)
        with netcdf_file('simple.nc', 'a') as f:
            assert_(not f.use_mmap)
            check_simple(f)
            assert_equal(f._attributes['appendRan'], 1)

        # Now without mmap
        with netcdf_file('simple.nc', mmap=False) as f:
            # Using mmap is the default
            assert_(not f.use_mmap)
            check_simple(f)

        # To read the NetCDF file we just created, as file object, no
        # mmap.  When n * n_bytes(var_type) is not divisible by 4, this
        # raised an error in pupynere 1.0.12 and scipy rev 5893, because
        # calculated vsize was rounding up in units of 4 - see
        # https://www.unidata.ucar.edu/software/netcdf/guide_toc.html
        with open('simple.nc', 'rb') as fobj:
            with netcdf_file(fobj) as f:
                # by default, don't use mmap for file-like
                assert_(not f.use_mmap)
                check_simple(f)

        # Read file from fileobj, with mmap
        with warnings.catch_warnings():
            with open('simple.nc', 'rb') as fobj:
                with netcdf_file(fobj, mmap=True) as f:
                    assert_(f.use_mmap)
                    check_simple(f)

        # Again read it in append mode (adding another att)
        with open('simple.nc', 'r+b') as fobj:
            with netcdf_file(fobj, 'a') as f:
                assert_(not f.use_mmap)
                check_simple(f)
                f.createDimension('app_dim', 1)
                var = f.createVariable('app_var', 'i', ('app_dim',))
                var[:] = 42

        # And... check that app_var made it in...
        with netcdf_file('simple.nc') as f:
            check_simple(f)
            assert_equal(f.variables['app_var'][:], 42)

    finally:
        os.chdir(cwd)
        shutil.rmtree(tmpdir)

