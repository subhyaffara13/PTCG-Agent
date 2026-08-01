
def recode_for_categories(
    codes: np.ndarray,
    old_categories,
    new_categories,
    *,
    copy: bool = True,
    warn: bool = False,
) -> np.ndarray:
    """
    Convert a set of codes for to a new set of categories

    Parameters
    ----------
    codes : np.ndarray
    old_categories, new_categories : Index
    copy: bool, default True
        Whether to copy if the codes are unchanged.
    warn : bool, default False
        Whether to warn on silent-NA mapping.

    Returns
    -------
    new_codes : np.ndarray[np.int64]

    Examples
    --------
    >>> old_cat = pd.Index(["b", "a", "c"])
    >>> new_cat = pd.Index(["a", "b"])
    >>> codes = np.array([0, 1, 1, 2])
    >>> recode_for_categories(codes, old_cat, new_cat, copy=True)
    array([ 1,  0,  0, -1], dtype=int8)
    """
    if len(old_categories) == 0:
        # All null anyway, so just retain the nulls
        if copy:
            return codes.copy()
        return codes
    elif new_categories.equals(old_categories):
        # Same categories, so no need to actually recode
        if copy:
            return codes.copy()
        return codes

    codes_in_old_cats = new_categories.get_indexer_for(old_categories)
    if warn:
        wrong = codes_in_old_cats == -1
        if wrong.any():
            warnings.warn(
                "Constructing a Categorical with a dtype and values containing "
                "non-null entries not in that dtype's categories is deprecated "
                "and will raise in a future version.",
                Pandas4Warning,
                stacklevel=find_stack_level(),
            )
    indexer = coerce_indexer_dtype(codes_in_old_cats, new_categories)
    new_codes = take_nd(indexer, codes, fill_value=-1)
    return new_codes

