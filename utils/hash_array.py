
def hash_array(
    vals: ArrayLike,
    encoding: str = "utf8",
    hash_key: str = _default_hash_key,
    categorize: bool = True,
) -> npt.NDArray[np.uint64]:
    """
    Given a 1d array, return an array of deterministic integers.

    Parameters
    ----------
    vals : ndarray or ExtensionArray
        The input array to hash.
    encoding : str, default 'utf8'
        Encoding for data & key when strings.
    hash_key : str, default _default_hash_key
        Hash_key for string key to encode.
    categorize : bool, default True
        Whether to first categorize object arrays before hashing. This is more
        efficient when the array contains duplicate values.

    Returns
    -------
    ndarray[np.uint64, ndim=1]
        Hashed values, same length as the vals.

    See Also
    --------
    util.hash_pandas_object : Return a data hash of the Index/Series/DataFrame.
    util.hash_tuples : Hash a MultiIndex / listlike-of-tuples efficiently.

    Examples
    --------
    >>> pd.util.hash_array(np.array([1, 2, 3]))
    array([ 6238072747940578789, 15839785061582574730,  2185194620014831856],
      dtype=uint64)
    """
    if not hasattr(vals, "dtype"):
        raise TypeError("must pass an ndarray-like")

    if isinstance(vals, ABCExtensionArray):
        return vals._hash_pandas_object(
            encoding=encoding, hash_key=hash_key, categorize=categorize
        )

    if not isinstance(vals, np.ndarray):
        # GH#42003
        raise TypeError(
            "hash_array requires np.ndarray or ExtensionArray, not "
            f"{type(vals).__name__}. Use hash_pandas_object instead."
        )

    return _hash_ndarray(vals, encoding, hash_key, categorize)

