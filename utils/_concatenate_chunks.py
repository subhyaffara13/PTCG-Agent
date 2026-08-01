
def _concatenate_chunks(
    chunks: list[dict[int, ArrayLike]], column_names: list[str]
) -> dict:
    """
    Concatenate chunks of data read with low_memory=True.

    The tricky part is handling Categoricals, where different chunks
    may have different inferred categories.
    """
    names = list(chunks[0].keys())
    warning_columns = []

    result: dict = {}
    for name in names:
        arrs = [chunk.pop(name) for chunk in chunks]
        # Check each arr for consistent types.
        dtypes = {a.dtype for a in arrs}
        non_cat_dtypes = {x for x in dtypes if not isinstance(x, CategoricalDtype)}

        dtype = dtypes.pop()
        if isinstance(dtype, CategoricalDtype):
            result[name] = union_categoricals(arrs, sort_categories=False)
        else:
            result[name] = concat_compat(arrs)
            if len(non_cat_dtypes) > 1 and result[name].dtype == np.dtype(object):
                warning_columns.append(column_names[name])

    if warning_columns:
        warning_names = ", ".join(
            [f"{index}: {name}" for index, name in enumerate(warning_columns)]
        )
        warning_message = " ".join(
            [
                f"Columns ({warning_names}) have mixed types. "
                f"Specify dtype option on import or set low_memory=False."
            ]
        )
        warnings.warn(warning_message, DtypeWarning, stacklevel=find_stack_level())
    return result

