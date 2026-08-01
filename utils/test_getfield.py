
def test_getfield():
    a = np.arange(32, dtype='uint16')
    if sys.byteorder == 'little':
        i = 0
        j = 1
    else:
        i = 1
        j = 0
    b = a.getfield('int8', i)
    assert_equal(b, a)
    b = a.getfield('int8', j)
    assert_equal(b, 0)
    pytest.raises(ValueError, a.getfield, 'uint8', -1)
    pytest.raises(ValueError, a.getfield, 'uint8', 16)
    pytest.raises(ValueError, a.getfield, 'uint64', 0)

