import copy

def test_gh_21022():
    # testing for absence of reported error
    source = np.ma.masked_array(data=[-1, -1], mask=True, dtype=np.float64)
    axis = np.array(0)
    result = np.prod(source, axis=axis, keepdims=False)
    result = np.ma.masked_array(result,
                                mask=np.ones(result.shape, dtype=np.bool))
    array = np.ma.masked_array(data=-1, mask=True, dtype=np.float64)
    copy.deepcopy(array)
    copy.deepcopy(result)

