
def is_all_strings(value: ArrayLike) -> bool:
    """
    Check if this is an array of strings that we should try parsing.

    Includes object-dtype ndarray containing all-strings, StringArray,
    and Categorical with all-string categories.
    Does not include numpy string dtypes.
    """
    dtype = value.dtype

    if isinstance(dtype, np.dtype):
        if len(value) == 0:
            return dtype == np.dtype("object")
        else:
            return dtype == np.dtype("object") and lib.is_string_array(
                np.asarray(value), skipna=False
            )
    elif isinstance(dtype, CategoricalDtype):
        return dtype.categories.inferred_type == "string"
    return dtype == "string"

