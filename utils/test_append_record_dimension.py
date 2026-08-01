
def test_append_recordDimension():
    dataSize = 100

    with in_tempdir():
        # Create file with record time dimension
        with netcdf_file('withRecordDimension.nc', 'w') as f:
            f.createDimension('time', None)
            f.createVariable('time', 'd', ('time',))
            f.createDimension('x', dataSize)
            x = f.createVariable('x', 'd', ('x',))
            x[:] = np.array(range(dataSize))
            f.createDimension('y', dataSize)
            y = f.createVariable('y', 'd', ('y',))
            y[:] = np.array(range(dataSize))
            f.createVariable('testData', 'i', ('time', 'x', 'y'))
            f.flush()
            f.close()

        for i in range(2):
            # Open the file in append mode and add data
            with netcdf_file('withRecordDimension.nc', 'a') as f:
                f.variables['time'].data = np.append(f.variables["time"].data, i)
                f.variables['testData'][i, :, :] = np.full((dataSize, dataSize), i)
                f.flush()

            # Read the file and check that append worked
            with netcdf_file('withRecordDimension.nc') as f:
                assert_equal(f.variables['time'][-1], i)
                assert_equal(f.variables['testData'][-1, :, :].copy(),
                             np.full((dataSize, dataSize), i))
                assert_equal(f.variables['time'].data.shape[0], i+1)
                assert_equal(f.variables['testData'].data.shape[0], i+1)

        # Read the file and check that 'data' was not saved as user defined
        # attribute of testData variable during append operation
        with netcdf_file('withRecordDimension.nc') as f:
            with assert_raises(KeyError) as ar:
                f.variables['testData']._attributes['data']
            ex = ar.value
            assert_equal(ex.args[0], 'data')

