
def test_fieldnames():
    # Check that field names are as expected
    stream = BytesIO()
    savemat(stream, {'a': {'a':1, 'b':2}})
    res = loadmat(stream)
    field_names = res['a'].dtype.names
    assert_equal(set(field_names), {'a', 'b'})

