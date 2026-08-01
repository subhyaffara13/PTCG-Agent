
def generate_shared_aggregator(
    func: Callable[..., Scalar],
    dtype_mapping: dict[np.dtype, np.dtype],
    is_grouped_kernel: bool,
    nopython: bool,
    nogil: bool,
    parallel: bool,
):
    """
    Generate a Numba function that loops over the columns 2D object and applies
    a 1D numba kernel over each column.

    Parameters
    ----------
    func : function
        aggregation function to be applied to each column
    dtype_mapping: dict or None
        If not None, maps a dtype to a result dtype.
        Otherwise, will fall back to default mapping.
    is_grouped_kernel: bool, default False
        Whether func operates using the group labels (True)
        or using starts/ends arrays

        If true, you also need to pass the number of groups to this function
    nopython : bool
        nopython to be passed into numba.jit
    nogil : bool
        nogil to be passed into numba.jit
    parallel : bool
        parallel to be passed into numba.jit

    Returns
    -------
    Numba function
    """

    # A wrapper around the looper function,
    # to dispatch based on dtype since numba is unable to do that in nopython mode

    # It also post-processes the values by inserting nans where number of observations
    # is less than min_periods
    # Cannot do this in numba nopython mode
    # (you'll run into type-unification error when you cast int -> float)
    def looper_wrapper(
        values,
        start=None,
        end=None,
        labels=None,
        ngroups=None,
        min_periods: int = 0,
        **kwargs,
    ):
        result_dtype = dtype_mapping[values.dtype]
        column_looper = make_looper(
            func, result_dtype, is_grouped_kernel, nopython, nogil, parallel
        )
        # Need to unpack kwargs since numba only supports *args
        if is_grouped_kernel:
            result, na_positions = column_looper(
                values, labels, ngroups, min_periods, *kwargs.values()
            )
        else:
            result, na_positions = column_looper(
                values, start, end, min_periods, *kwargs.values()
            )
        if result.dtype.kind == "i":
            # Look if na_positions is not empty
            # If so, convert the whole block
            # This is OK since int dtype cannot hold nan,
            # so if min_periods not satisfied for 1 col, it is not satisfied for
            # all columns at that index
            for na_pos in na_positions.values():
                if len(na_pos) > 0:
                    result = result.astype("float64")
                    break
        # TODO: Optimize this
        for i, na_pos in na_positions.items():
            if len(na_pos) > 0:
                result[i, na_pos] = np.nan
        return result

    return looper_wrapper

