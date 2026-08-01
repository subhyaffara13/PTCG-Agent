
def _maybe_promote(dtype: np.dtype, fill_value=np.nan):
    # The actual implementation of the function, use `maybe_promote` above for
    # a cached version.
    if not is_scalar(fill_value):
        # with object dtype there is nothing to promote, and the user can
        #  pass pretty much any weird fill_value they like
        if dtype != object:
            # with object dtype there is nothing to promote, and the user can
            #  pass pretty much any weird fill_value they like
            raise ValueError("fill_value must be a scalar")
        dtype = _dtype_obj
        return dtype, fill_value

    if is_valid_na_for_dtype(fill_value, dtype) and dtype.kind in "iufcmM":
        dtype = ensure_dtype_can_hold_na(dtype)
        fv = na_value_for_dtype(dtype)
        return dtype, fv

    elif isinstance(dtype, CategoricalDtype):
        if fill_value in dtype.categories or isna(fill_value):
            return dtype, fill_value
        else:
            return object, ensure_object(fill_value)

    elif isna(fill_value):
        dtype = _dtype_obj
        if fill_value is None:
            # but we retain e.g. pd.NA
            fill_value = np.nan
        return dtype, fill_value

    # returns tuple of (dtype, fill_value)
    if issubclass(dtype.type, np.datetime64):
        inferred, fv = infer_dtype_from_scalar(fill_value)
        if inferred == dtype:
            return dtype, fv

        from pandas.core.arrays import DatetimeArray

        dta = DatetimeArray._from_sequence([], dtype="M8[ns]")
        try:
            fv = dta._validate_setitem_value(fill_value)
            return dta.dtype, fv
        except (ValueError, TypeError):
            return _dtype_obj, fill_value

    elif issubclass(dtype.type, np.timedelta64):
        inferred, fv = infer_dtype_from_scalar(fill_value)
        if inferred == dtype:
            return dtype, fv

        elif inferred.kind == "m":
            # different unit, e.g. passed np.timedelta64(24, "h") with dtype=m8[ns]
            # see if we can losslessly cast it to our dtype
            unit = np.datetime_data(dtype)[0]
            unit = cast("TimeUnit", unit)
            try:
                td = Timedelta(fill_value).as_unit(unit, round_ok=False)
            except OutOfBoundsTimedelta:
                return _dtype_obj, fill_value
            else:
                return dtype, td.asm8

        return _dtype_obj, fill_value

    elif is_float(fill_value):
        if issubclass(dtype.type, np.bool_):
            dtype = np.dtype(np.object_)

        elif issubclass(dtype.type, np.integer):
            dtype = np.dtype(np.float64)

        elif dtype.kind == "f":
            mst = np.min_scalar_type(fill_value)
            if mst > dtype:
                # e.g. mst is np.float64 and dtype is np.float32
                dtype = mst

        elif dtype.kind == "c":
            mst = np.min_scalar_type(fill_value)
            dtype = np.promote_types(dtype, mst)

    elif is_bool(fill_value):
        if not issubclass(dtype.type, np.bool_):
            dtype = np.dtype(np.object_)

    elif is_integer(fill_value):
        if issubclass(dtype.type, np.bool_):
            dtype = np.dtype(np.object_)

        elif issubclass(dtype.type, np.integer):
            if not np_can_cast_scalar(fill_value, dtype):
                # upcast to prevent overflow
                mst = np.min_scalar_type(fill_value)
                dtype = np.promote_types(dtype, mst)
                if dtype.kind == "f":
                    # Case where we disagree with numpy
                    dtype = np.dtype(np.object_)

    elif is_complex(fill_value):
        if issubclass(dtype.type, np.bool_):
            dtype = np.dtype(np.object_)

        elif issubclass(dtype.type, (np.integer, np.floating)):
            mst = np.min_scalar_type(fill_value)
            dtype = np.promote_types(dtype, mst)

        elif dtype.kind == "c":
            mst = np.min_scalar_type(fill_value)
            if mst > dtype:
                # e.g. mst is np.complex128 and dtype is np.complex64
                dtype = mst

    else:
        dtype = np.dtype(np.object_)

    # in case we have a string that looked like a number
    if issubclass(dtype.type, (bytes, str)):
        dtype = np.dtype(np.object_)

    fill_value = _ensure_dtype_type(fill_value, dtype)
    return dtype, fill_value

