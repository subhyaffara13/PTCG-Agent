
def reorder_arrays(
    arrays: list[ArrayLike], arr_columns: Index, columns: Index | None, length: int
) -> tuple[list[ArrayLike], Index]:
    """
    Preemptively (cheaply) reindex arrays with new columns.
    """
    # reorder according to the columns
    if columns is not None:
        if not columns.equals(arr_columns):
            # if they are equal, there is nothing to do
            new_arrays: list[ArrayLike] = []
            indexer = arr_columns.get_indexer(columns)
            for i, k in enumerate(indexer):
                if k == -1:
                    # by convention default is all-NaN object dtype
                    arr = np.empty(length, dtype=object)
                    arr.fill(np.nan)
                else:
                    arr = arrays[k]
                new_arrays.append(arr)

            arrays = new_arrays
            arr_columns = columns

    return arrays, arr_columns

