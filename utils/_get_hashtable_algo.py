
def _get_hashtable_algo(
    values: np.ndarray,
) -> tuple[type[htable.HashTable], np.ndarray]:
    """
    Parameters
    ----------
    values : np.ndarray

    Returns
    -------
    htable : HashTable subclass
    values : ndarray
    """
    values = _ensure_data(values)

    ndtype = _check_object_for_strings(values)
    hashtable = _hashtables[ndtype]
    return hashtable, values

