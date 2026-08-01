
def box_expected(expected, box_cls, transpose: bool = True):
    """
    Helper function to wrap the expected output of a test in a given box_class.

    Parameters
    ----------
    expected : np.ndarray, Index, Series
    box_cls : {Index, Series, DataFrame}

    Returns
    -------
    subclass of box_cls
    """
    if box_cls is pd.array:
        if isinstance(expected, RangeIndex):
            # pd.array would return an IntegerArray
            expected = NumpyExtensionArray(np.asarray(expected._values))
        else:
            expected = pd.array(expected, copy=False)
    elif box_cls is Index:
        expected = Index(expected, copy=False)
    elif box_cls is Series:
        expected = Series(expected)
    elif box_cls is DataFrame:
        expected = Series(expected).to_frame()
        if transpose:
            # for vector operations, we need a DataFrame to be a single-row,
            #  not a single-column, in order to operate against non-DataFrame
            #  vectors of the same length. But convert to two rows to avoid
            #  single-row special cases in datetime arithmetic
            expected = expected.T
            expected = pd.concat([expected] * 2, ignore_index=True)
    elif box_cls is np.ndarray or box_cls is np.array:
        expected = np.array(expected)
    elif box_cls is to_array:
        expected = to_array(expected)
    else:
        raise NotImplementedError(box_cls)
    return expected

