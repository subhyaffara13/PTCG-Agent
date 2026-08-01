
def test_array_interface_unicode_typestr():
    arr = np.array([1, 2, 3], dtype='int32')
    interface = dict(arr.__array_interface__)
    interface['typestr'] = '\N{check mark}'

    class DummyArray:
        __array_interface__ = interface

    # should not be UnicodeEncodeError
    with pytest.raises(TypeError):
        np.asarray(DummyArray())

