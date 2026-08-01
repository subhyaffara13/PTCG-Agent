
def _list_of_dict_to_arrays(
    data: list[dict],
    columns: Index | None,
) -> tuple[np.ndarray, Index]:
    """
    Convert list of dicts to numpy arrays

    if `columns` is not passed, column names are inferred from the records
    - for OrderedDict and dicts, the column names match
      the key insertion-order from the first record to the last.
    - For other kinds of dict-likes, the keys are lexically sorted.

    Parameters
    ----------
    data : iterable
        collection of records (OrderedDict, dict)
    columns: iterables or None

    Returns
    -------
    content : np.ndarray[object, ndim=2]
    columns : Index
    """
    # assure that they are of the base dict class and not of derived
    # classes
    data = [d if type(d) is dict else dict(d) for d in data]

    if columns is None:
        gen = (list(x.keys()) for x in data)
        sort = not any(isinstance(d, dict) for d in data)
        pre_cols = lib.fast_unique_multiple_list_gen(gen, sort=sort)
        columns = ensure_index(pre_cols)

        # use pre_cols to preserve exact values that were present as dict keys
        # (e.g. otherwise missing values might be coerced to the canonical repr)
        content = lib.dicts_to_array(data, pre_cols)
    else:
        content = lib.dicts_to_array(data, list(columns))

    return content, columns

