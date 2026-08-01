
def sum_labels(input, labels=None, index=None):
    """
    Calculate the sum of the values of the array.

    Parameters
    ----------
    input : array_like
        Values of `input` inside the regions defined by `labels`
        are summed together.
    labels : array_like of ints, optional
        Assign labels to the values of the array. Has to have the same shape as
        `input`.
    index : array_like, optional
        A single label number or a sequence of label numbers of
        the objects to be measured.

    Returns
    -------
    sum : ndarray or scalar
        An array of the sums of values of `input` inside the regions defined
        by `labels` with the same shape as `index`. If 'index' is None or scalar,
        a scalar is returned.

    See Also
    --------
    mean, median

    Examples
    --------
    >>> from scipy import ndimage
    >>> input =  [0,1,2,3]
    >>> labels = [1,1,2,2]
    >>> ndimage.sum_labels(input, labels, index=[1,2])
    [1.0, 5.0]
    >>> ndimage.sum_labels(input, labels, index=1)
    1
    >>> ndimage.sum_labels(input, labels)
    6


    """
    count, sum = _stats(input, labels, index)
    return sum

