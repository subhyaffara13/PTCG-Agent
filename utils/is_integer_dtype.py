
def is_integer_dtype(dtype: numpy.typing.DTypeLike) -> bool:
  """Returns whether the given dtype is an integer dtype.

  Supports both basic numpy dtypes and the extended dtypes in the `ml_dtypes`
  package (if installed).

  Args:
    dtype: The dtype to check.

  Returns:
    True if the given dtype is an integer dtype.
  """
  dtype = np.dtype(dtype)
  if np.issubdtype(dtype, np.integer):
    return True
  if isinstance(dtype.type, type) and dtype.type.__module__ == "ml_dtypes":
    import ml_dtypes  # pylint: disable=import-outside-toplevel

    try:
      _ = ml_dtypes.iinfo(dtype)
      return True
    except ValueError:
      return False
  return False


def is_integer_dtype(dtype: torch.dtype) -> bool:
    if not isinstance(dtype, torch.dtype):
        raise AssertionError(f"Expected torch.dtype, got {type(dtype)}")
    return dtype in _integer_dtypes


def is_integer_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of an integer dtype.

    Unlike in `is_any_int_dtype`, timedelta64 instances will return False.

    The nullable Integer dtypes (e.g. pandas.Int64Dtype) are also considered
    as integer by this function.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array or dtype is of an integer dtype and
        not an instance of timedelta64.

    See Also
    --------
    api.types.is_integer : Return True if given object is integer.
    api.types.is_numeric_dtype : Check whether the provided array or dtype is of a
        numeric dtype.
    api.types.is_float_dtype : Check whether the provided array or dtype is of a
        float dtype.
    Int64Dtype : An ExtensionDtype for Int64Dtype integer data.

    Examples
    --------
    >>> from pandas.api.types import is_integer_dtype
    >>> is_integer_dtype(str)
    False
    >>> is_integer_dtype(int)
    True
    >>> is_integer_dtype(float)
    False
    >>> is_integer_dtype(np.uint64)
    True
    >>> is_integer_dtype("int8")
    True
    >>> is_integer_dtype("Int8")
    True
    >>> is_integer_dtype(pd.Int8Dtype)
    True
    >>> is_integer_dtype(np.datetime64)
    False
    >>> is_integer_dtype(np.timedelta64)
    False
    >>> is_integer_dtype(np.array(["a", "b"]))
    False
    >>> is_integer_dtype(pd.Series([1, 2]))
    True
    >>> is_integer_dtype(np.array([], dtype="m8[ns]"))
    False
    >>> is_integer_dtype(pd.Index([1, 2.0]))  # float
    False
    """
    return _is_dtype_type(
        arr_or_dtype, _classes_and_not_datetimelike(np.integer)
    ) or _is_dtype(
        arr_or_dtype, lambda typ: isinstance(typ, ExtensionDtype) and typ.kind in "iu"
    )

