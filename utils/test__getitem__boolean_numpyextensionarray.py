
def test__getitem__boolean_numpyextensionarray():
    ri = RangeIndex(1)
    result = ri[pd.arrays.NumpyExtensionArray(np.array([True]))]
    tm.assert_index_equal(ri, result)

