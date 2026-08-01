
def assert_mask_matches(arr, expected_mask):
    '''
    Asserts that the mask of arr is effectively the same as expected_mask.

    In contrast to numpy.ma.testutils.assert_mask_equal, this function allows
    testing the 'mask' of a standard numpy array (the mask in this case is treated
    as all False).

    Parameters
    ----------
    arr : ndarray or MaskedArray
        Array to test.
    expected_mask : array_like of booleans
        A list giving the expected mask.
    '''

    mask = np.ma.getmaskarray(arr)
    assert_equal(mask, expected_mask)

