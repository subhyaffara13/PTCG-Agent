
def label(input, structure=None, output=None):
    """
    Label features in an array.

    Parameters
    ----------
    input : array_like
        An array-like object to be labeled. Any non-zero values in `input` are
        counted as features and zero values are considered the background.
    structure : array_like, optional
        A structuring element that defines feature connections.
        `structure` must be centrosymmetric
        (see Notes).
        If no structuring element is provided,
        one is automatically generated with a squared connectivity equal to
        one.  That is, for a 2-D `input` array, the default structuring element
        is::

            [[0,1,0],
             [1,1,1],
             [0,1,0]]

    output : (None, data-type, array_like), optional
        If `output` is a data type, it specifies the type of the resulting
        labeled feature array.
        If `output` is an array-like object, then `output` will be updated
        with the labeled features from this function.  This function can
        operate in-place, by passing output=input.
        Note that the output must be able to store the largest label, or this
        function will raise an Exception.

    Returns
    -------
    label : ndarray or int
        An integer ndarray where each unique feature in `input` has a unique
        label in the returned array.
    num_features : int
        How many objects were found.

        If `output` is None, this function returns a tuple of
        (`labeled_array`, `num_features`).

        If `output` is an ndarray, then it will be updated with values in
        `labeled_array` and only `num_features` will be returned by this
        function.

    See Also
    --------
    find_objects : generate a list of slices for the labeled features (or
                   objects); useful for finding features' position or
                   dimensions

    Notes
    -----
    A centrosymmetric matrix is a matrix that is symmetric about the center.
    See [1]_ for more information.

    The `structure` matrix must be centrosymmetric to ensure
    two-way connections.
    For instance, if the `structure` matrix is not centrosymmetric
    and is defined as::

        [[0,1,0],
         [1,1,0],
         [0,0,0]]

    and the `input` is::

        [[1,2],
         [0,3]]

    then the structure matrix would indicate the
    entry 2 in the input is connected to 1,
    but 1 is not connected to 2.

    References
    ----------
    .. [1] James R. Weaver, "Centrosymmetric (cross-symmetric)
       matrices, their basic properties, eigenvalues, and
       eigenvectors." The American Mathematical Monthly 92.10
       (1985): 711-717.

    Examples
    --------
    Create an image with some features, then label it using the default
    (cross-shaped) structuring element:

    >>> from scipy.ndimage import label, generate_binary_structure
    >>> import numpy as np
    >>> a = np.array([[0,0,1,1,0,0],
    ...               [0,0,0,1,0,0],
    ...               [1,1,0,0,1,0],
    ...               [0,0,0,1,0,0]])
    >>> labeled_array, num_features = label(a)

    Each of the 4 features are labeled with a different integer:

    >>> num_features
    4
    >>> labeled_array
    array([[0, 0, 1, 1, 0, 0],
           [0, 0, 0, 1, 0, 0],
           [2, 2, 0, 0, 3, 0],
           [0, 0, 0, 4, 0, 0]], dtype=int32)

    Generate a structuring element that will consider features connected even
    if they touch diagonally:

    >>> s = generate_binary_structure(2,2)

    or,

    >>> s = [[1,1,1],
    ...      [1,1,1],
    ...      [1,1,1]]

    Label the image using the new structuring element:

    >>> labeled_array, num_features = label(a, structure=s)

    Show the 2 labeled features (note that features 1, 3, and 4 from above are
    now considered a single feature):

    >>> num_features
    2
    >>> labeled_array
    array([[0, 0, 1, 1, 0, 0],
           [0, 0, 0, 1, 0, 0],
           [2, 2, 0, 0, 1, 0],
           [0, 0, 0, 1, 0, 0]], dtype=int32)

    """
    input = np.asarray(input)
    if np.iscomplexobj(input):
        raise TypeError('Complex type not supported')
    if structure is None:
        structure = _morphology.generate_binary_structure(input.ndim, 1)
    structure = np.asarray(structure, dtype=bool)
    if structure.ndim != input.ndim:
        raise RuntimeError('structure and input must have equal rank')
    for ii in structure.shape:
        if ii != 3:
            raise ValueError('structure dimensions must be equal to 3')

    # Use 32 bits if it's large enough for this image.
    # _ni_label.label() needs two entries for background and
    # foreground tracking
    need_64bits = input.size >= (2**31 - 2)

    if isinstance(output, np.ndarray):
        if output.shape != input.shape:
            raise ValueError("output shape not correct")
        caller_provided_output = True
    else:
        caller_provided_output = False
        if output is None:
            output = np.empty(input.shape, np.intp if need_64bits else np.int32)
        else:
            output = np.empty(input.shape, output)

    # handle scalars, 0-D arrays
    if input.ndim == 0 or input.size == 0:
        if input.ndim == 0:
            # scalar
            maxlabel = 1 if (input != 0) else 0
            output[...] = maxlabel
        else:
            # 0-D
            maxlabel = 0
        if caller_provided_output:
            return maxlabel
        else:
            return output, maxlabel

    try:
        max_label = _ni_label._label(input, structure, output)
    except _ni_label.NeedMoreBits as e:
        # Make another attempt with enough bits, then try to cast to the
        # new type.
        tmp_output = np.empty(input.shape, np.intp if need_64bits else np.int32)
        max_label = _ni_label._label(input, structure, tmp_output)
        output[...] = tmp_output[...]
        if not np.all(output == tmp_output):
            # refuse to return bad results
            raise RuntimeError(
                "insufficient bit-depth in requested output type"
            ) from e

    if caller_provided_output:
        # result was written in-place
        return max_label
    else:
        return output, max_label

