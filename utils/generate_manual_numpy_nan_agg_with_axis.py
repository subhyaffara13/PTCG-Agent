
def generate_manual_numpy_nan_agg_with_axis(nan_func):
    if TYPE_CHECKING:
        import numba
    else:
        numba = import_optional_dependency("numba")

    @numba.jit(nopython=True, nogil=True, parallel=True)
    def nan_agg_with_axis(table):
        result = np.empty(table.shape[1])
        for i in numba.prange(table.shape[1]):
            partition = table[:, i]
            result[i] = nan_func(partition)
        return result

    return nan_agg_with_axis

