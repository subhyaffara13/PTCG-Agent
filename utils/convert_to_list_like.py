
def convert_to_list_like(
    values: Hashable | Iterable | AnyArrayLike,
) -> list | AnyArrayLike:
    """
    Convert list-like or scalar input to list-like. List, numpy and pandas array-like
    inputs are returned unmodified whereas others are converted to list.
    """
    if isinstance(values, (list, np.ndarray, ABCIndex, ABCSeries, ABCExtensionArray)):
        return values
    elif isinstance(values, abc.Iterable) and not isinstance(values, str):
        return list(values)

    return [values]

