
def generate_numba_table_func(
    func: Callable[..., np.ndarray],
    nopython: bool,
    nogil: bool,
    parallel: bool,
):
    """
    Generate a numba jitted function to apply window calculations table-wise.

    Func will be passed an M window size x N number of columns array, and
    must return a 1 x N number of columns array.

    1. jit the user's function
    2. Return a rolling apply function with the jitted function inline

    Parameters
    ----------
    func : function
        function to be applied to each window and will be JITed
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
    numba_func = jit_user_function(func)
    if TYPE_CHECKING:
        import numba
    else:
        numba = import_optional_dependency("numba")

    @numba.jit(nopython=nopython, nogil=nogil, parallel=parallel)
    def roll_table(
        values: np.ndarray,
        begin: np.ndarray,
        end: np.ndarray,
        minimum_periods: int,
        *args: Any,
    ):
        result = np.empty((len(begin), values.shape[1]))
        min_periods_mask = np.empty(result.shape)
        for i in numba.prange(len(result)):
            start = begin[i]
            stop = end[i]
            window = values[start:stop]
            count_nan = np.sum(np.isnan(window), axis=0)
            nan_mask = len(window) - count_nan >= minimum_periods
            if nan_mask.any():
                result[i, :] = numba_func(window, *args)
            min_periods_mask[i, :] = nan_mask
        result = np.where(min_periods_mask, result, np.nan)
        return result

    return roll_table

