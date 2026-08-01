
def test_encoded_fill_value():
    with netcdf_file(BytesIO(), mode='w') as f:
        f.createDimension('x', 1)
        var = f.createVariable('var', 'S1', ('x',))
        assert_equal(var._get_encoded_fill_value(), b'\x00')
        var._FillValue = b'\x01'
        assert_equal(var._get_encoded_fill_value(), b'\x01')
        var._FillValue = b'\x00\x00'  # invalid, wrong size
        assert_equal(var._get_encoded_fill_value(), b'\x00')

