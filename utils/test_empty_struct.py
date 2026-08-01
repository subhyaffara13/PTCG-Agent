
def test_empty_struct():
    # ticket 885
    filename = pjoin(test_data_path,'test_empty_struct.mat')
    # before ticket fix, this would crash with ValueError, empty data
    # type
    d = loadmat(filename, struct_as_record=True)
    a = d['a']
    assert_equal(a.shape, (1,1))
    assert_equal(a.dtype, np.dtype(object))
    assert_(a[0,0] is None)
    stream = BytesIO()
    arr = np.array((), dtype='U')
    # before ticket fix, this used to give data type not understood
    savemat(stream, {'arr':arr})
    d = loadmat(stream)
    a2 = d['arr']
    assert_array_equal(a2, arr)

