
def test_array_interface_itemsize():
    # See gh-6361
    my_dtype = np.dtype({'names': ['A', 'B'], 'formats': ['f4', 'f4'],
                         'offsets': [0, 8], 'itemsize': 16})
    a = np.ones(10, dtype=my_dtype)
    descr_t = np.dtype(a.__array_interface__['descr'])
    typestr_t = np.dtype(a.__array_interface__['typestr'])
    assert_equal(descr_t.itemsize, typestr_t.itemsize)

