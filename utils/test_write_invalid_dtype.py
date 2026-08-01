
def test_write_invalid_dtype():
    dtypes = ['int64', 'uint64']
    if np.dtype('int').itemsize == 8:   # 64-bit machines
        dtypes.append('int')
    if np.dtype('uint').itemsize == 8:   # 64-bit machines
        dtypes.append('uint')

    with netcdf_file(BytesIO(), 'w') as f:
        f.createDimension('time', N_EG_ELS)
        for dt in dtypes:
            assert_raises(ValueError, f.createVariable, 'time', dt, ('time',))

