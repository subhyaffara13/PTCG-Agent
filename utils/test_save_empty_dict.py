
def test_save_empty_dict():
    # saving empty dict also gives empty struct
    stream = BytesIO()
    savemat(stream, {'arr': {}})
    d = loadmat(stream)
    a = d['arr']
    assert_equal(a.shape, (1,1))
    assert_equal(a.dtype, np.dtype(object))
    assert_(a[0,0] is None)

