from typing import Callable

def ensure_key_mapped(
    values: ArrayLike | Index | Series, key: Callable | None, levels=None
) -> ArrayLike | Index | Series:
    """
    Applies a callable key function to the values function and checks
    that the resulting value has the same shape. Can be called on Index
    subclasses, Series, DataFrames, or ndarrays.

    Parameters
    ----------
    values : Series, DataFrame, Index subclass, or ndarray
    key : Optional[Callable], key to be called on the values array
    levels : Optional[List], if values is a MultiIndex, list of levels to
    apply the key to.
    """
    from pandas.core.indexes.api import Index

    if not key:
        return values

    if isinstance(values, ABCMultiIndex):
        return _ensure_key_mapped_multiindex(values, key, level=levels)

    result = key(values.copy())
    if len(result) != len(values):
        raise ValueError(
            "User-provided `key` function must not change the shape of the array."
        )

    try:
        if isinstance(
            values, Index
        ):  # convert to a new Index subclass, not necessarily the same
            result = Index(result, tupleize_cols=False)
        else:
            # try to revert to original type otherwise
            type_of_values = type(values)
            #  error: Too many arguments for "ExtensionArray"
            result = type_of_values(result)  # type: ignore[call-arg]
    except TypeError as err:
        raise TypeError(
            f"User-provided `key` function returned an invalid type {type(result)} \
            which could not be converted to {type(values)}."
        ) from err

    return result

