
def test_save_dict():
    # Test that both dict and OrderedDict can be saved (as recarray),
    # loaded as matstruct, and preserve order
    ab_exp = np.array([[(1, 2)]], dtype=[('a', object), ('b', object)])
    for dict_type in (dict, OrderedDict):
        # Initialize with tuples to keep order
        d = dict_type([('a', 1), ('b', 2)])
        stream = BytesIO()
        savemat(stream, {'dict': d})
        stream.seek(0)
        vals = loadmat(stream)['dict']
        assert_equal(vals.dtype.names, ('a', 'b'))
        assert_array_equal(vals, ab_exp)

