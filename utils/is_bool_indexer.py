
def is_bool_indexer(key: Any) -> bool:
    """
    Check whether `key` is a valid boolean indexer.

    Parameters
    ----------
    key : Any
        Only list-likes may be considered boolean indexers.
        All other types are not considered a boolean indexer.
        For array-like input, boolean ndarrays or ExtensionArrays
        with ``_is_boolean`` set are considered boolean indexers.

    Returns
    -------
    bool
        Whether `key` is a valid boolean indexer.

    Raises
    ------
    ValueError
        When the array is an object-dtype ndarray or ExtensionArray
        and contains missing values.

    See Also
    --------
    check_array_indexer : Check that `key` is a valid array to index,
        and convert to an ndarray.
    """
    if isinstance(
        key,
        (ABCSeries, np.ndarray, ABCIndex, ABCExtensionArray, ABCNumpyExtensionArray),
    ) and not isinstance(key, ABCMultiIndex):
        if key.dtype == np.object_:
            key_array = np.asarray(key)

            if not lib.is_bool_array(key_array):
                na_msg = "Cannot mask with non-boolean array containing NA / NaN values"
                if lib.is_bool_array(key_array, skipna=True):
                    # Don't raise on e.g. ["A", "B", np.nan], see
                    #  test_loc_getitem_list_of_labels_categoricalindex_with_na
                    raise ValueError(na_msg)
                return False
            return True
        elif is_bool_dtype(key.dtype):
            return True
    elif isinstance(key, list):
        # check if np.array(key).dtype would be bool
        if len(key) > 0:
            if type(key) is not list:
                # GH#42461 cython will raise TypeError if we pass a subclass
                key = list(key)
            return lib.is_bool_list(key)

    return False

