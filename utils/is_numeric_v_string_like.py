
def is_numeric_v_string_like(a: ArrayLike, b) -> bool:
    """
    Check if we are comparing a string-like object to a numeric ndarray.
    NumPy doesn't like to compare such objects, especially numeric arrays
    and scalar string-likes.

    Parameters
    ----------
    a : array-like, scalar
        The first object to check.
    b : array-like, scalar
        The second object to check.

    Returns
    -------
    boolean
        Whether we return a comparing a string-like object to a numeric array.

    Examples
    --------
    >>> is_numeric_v_string_like(np.array([1]), "foo")
    True
    >>> is_numeric_v_string_like(np.array([1, 2]), np.array(["foo"]))
    True
    >>> is_numeric_v_string_like(np.array(["foo"]), np.array([1, 2]))
    True
    >>> is_numeric_v_string_like(np.array([1]), np.array([2]))
    False
    >>> is_numeric_v_string_like(np.array(["foo"]), np.array(["foo"]))
    False
    """
    is_a_array = isinstance(a, np.ndarray)
    is_b_array = isinstance(b, np.ndarray)

    is_a_numeric_array = is_a_array and a.dtype.kind in "uifcb"
    is_b_numeric_array = is_b_array and b.dtype.kind in "uifcb"
    is_a_string_array = is_a_array and a.dtype.kind in "SU"
    is_b_string_array = is_b_array and b.dtype.kind in "SU"

    is_b_scalar_string_like = not is_b_array and isinstance(b, str)

    return (
        (is_a_numeric_array and is_b_scalar_string_like)
        or (is_a_numeric_array and is_b_string_array)
        or (is_b_numeric_array and is_a_string_array)
    )

