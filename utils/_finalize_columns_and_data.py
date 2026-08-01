
def _finalize_columns_and_data(
    content: np.ndarray,  # ndim == 2
    columns: Index | None,
    dtype: DtypeObj | None,
) -> tuple[list[ArrayLike], Index]:
    """
    Ensure we have valid columns, cast object dtypes if possible.
    """
    contents = list(content.T)

    try:
        columns = _validate_or_indexify_columns(contents, columns)
    except AssertionError as err:
        # GH#26429 do not raise user-facing AssertionError
        raise ValueError(err) from err

    if contents and contents[0].dtype == np.object_:
        contents = convert_object_array(contents, dtype=dtype)

    return contents, columns

