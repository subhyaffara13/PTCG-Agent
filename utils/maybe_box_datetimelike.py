
def maybe_box_datetimelike(value: Scalar, dtype: Dtype | None = None) -> Scalar:
    """
    Cast scalar to Timestamp or Timedelta if scalar is datetime-like
    and dtype is not object.

    Parameters
    ----------
    value : scalar
    dtype : Dtype, optional

    Returns
    -------
    scalar
    """
    if dtype == _dtype_obj:
        pass
    elif isinstance(value, (np.datetime64, dt.datetime)):
        value = Timestamp(value)
    elif isinstance(value, (np.timedelta64, dt.timedelta)):
        value = Timedelta(value)

    return value

