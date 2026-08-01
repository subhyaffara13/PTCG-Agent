
def _nbins_to_bins(x_idx: Index, nbins: int, right: bool) -> Index:
    """
    If a user passed an integer N for bins, convert this to a sequence of N
    equal(ish)-sized bins.
    """
    if is_scalar(nbins) and nbins < 1:
        raise ValueError("`bins` should be a positive integer.")

    if x_idx.size == 0:
        raise ValueError("Cannot cut empty array")

    rng = (x_idx.min(), x_idx.max())
    mn, mx = rng

    if is_numeric_dtype(x_idx.dtype) and (np.isinf(mn) or np.isinf(mx)):
        # GH#24314
        raise ValueError(
            "cannot specify integer `bins` when input data contains infinity"
        )

    if mn == mx:  # adjust end points before binning
        if _is_dt_or_td(x_idx.dtype):
            # using seconds=1 is pretty arbitrary here
            # error: Argument 1 to "dtype_to_unit" has incompatible type
            # "dtype[Any] | ExtensionDtype"; expected "DatetimeTZDtype | dtype[Any]"
            unit = dtype_to_unit(x_idx.dtype)  # type: ignore[arg-type]
            td = Timedelta(seconds=1).as_unit(cast("TimeUnit", unit))
            # Use DatetimeArray/TimedeltaArray method instead of linspace
            # error: Item "ExtensionArray" of "ExtensionArray | ndarray[Any, Any]"
            # has no attribute "_generate_range"
            bins = x_idx._values._generate_range(  # type: ignore[union-attr]
                start=mn - td, end=mx + td, periods=nbins + 1, freq=None, unit=unit
            )
        else:
            mn -= 0.001 * abs(mn) if mn != 0 else 0.001
            mx += 0.001 * abs(mx) if mx != 0 else 0.001

            bins = np.linspace(mn, mx, nbins + 1, endpoint=True)
    else:  # adjust end points after binning
        if _is_dt_or_td(x_idx.dtype):
            # Use DatetimeArray/TimedeltaArray method instead of linspace

            # error: Argument 1 to "dtype_to_unit" has incompatible type
            # "dtype[Any] | ExtensionDtype"; expected "DatetimeTZDtype | dtype[Any]"
            unit = dtype_to_unit(x_idx.dtype)  # type: ignore[arg-type]
            # error: Item "ExtensionArray" of "ExtensionArray | ndarray[Any, Any]"
            # has no attribute "_generate_range"
            bins = x_idx._values._generate_range(  # type: ignore[union-attr]
                start=mn, end=mx, periods=nbins + 1, freq=None, unit=unit
            )
        else:
            bins = np.linspace(mn, mx, nbins + 1, endpoint=True)
        adj = (mx - mn) * 0.001  # 0.1% of the range
        if right:
            bins[0] -= adj
        else:
            bins[-1] += adj

    return Index(bins, copy=False)

