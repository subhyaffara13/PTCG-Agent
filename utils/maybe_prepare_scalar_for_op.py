
def maybe_prepare_scalar_for_op(obj, shape: Shape):
    """
    Cast non-pandas objects to pandas types to unify behavior of arithmetic
    and comparison operations.

    Parameters
    ----------
    obj: object
    shape : tuple[int]

    Returns
    -------
    out : object

    Notes
    -----
    Be careful to call this *after* determining the `name` attribute to be
    attached to the result of the arithmetic operation.
    """
    if type(obj) is datetime.timedelta:
        # GH#22390  cast up to Timedelta to rely on Timedelta
        # implementation; otherwise operation against numeric-dtype
        # raises TypeError
        return Timedelta(obj)
    elif type(obj) is datetime.datetime:
        # cast up to Timestamp to rely on Timestamp implementation, see Timedelta above
        return Timestamp(obj)
    elif isinstance(obj, np.datetime64):
        # GH#28080 numpy casts integer-dtype to datetime64 when doing
        #  array[int] + datetime64, which we do not allow
        if isna(obj):
            from pandas.core.arrays import DatetimeArray

            # Avoid possible ambiguities with pd.NaT
            # GH 52295
            if is_unitless(obj.dtype):
                # Use second resolution to ensure that the result of e.g.
                #  `left - np.datetime64("NaT")` retains the unit of left.unit
                obj = obj.astype("datetime64[s]")
            elif not is_supported_dtype(obj.dtype):
                new_dtype = get_supported_dtype(obj.dtype)
                obj = obj.astype(new_dtype)
            right = np.broadcast_to(obj, shape)
            return DatetimeArray._simple_new(right, dtype=right.dtype)

        return Timestamp(obj)

    elif isinstance(obj, np.timedelta64):
        if isna(obj):
            from pandas.core.arrays import TimedeltaArray

            # wrapping timedelta64("NaT") in Timedelta returns NaT,
            #  which would incorrectly be treated as a datetime-NaT, so
            #  we broadcast and wrap in a TimedeltaArray
            # GH 52295
            if is_unitless(obj.dtype):
                # Use second resolution to ensure that the result of e.g.
                #  `left + np.timedelta64("NaT")` retains the unit of left.unit
                obj = obj.astype("timedelta64[s]")
            elif not is_supported_dtype(obj.dtype):
                new_dtype = get_supported_dtype(obj.dtype)
                obj = obj.astype(new_dtype)
            right = np.broadcast_to(obj, shape)
            return TimedeltaArray._simple_new(right, dtype=right.dtype)

        # In particular non-nanosecond timedelta64 needs to be cast to
        #  nanoseconds, or else we get undesired behavior like
        #  np.timedelta64(3, 'D') / 2 == np.timedelta64(1, 'D')
        return Timedelta(obj)

    # We want NumPy numeric scalars to behave like Python scalars
    # post NEP 50
    elif isinstance(obj, np.integer):
        return int(obj)

    elif isinstance(obj, np.floating):
        return float(obj)

    return obj

