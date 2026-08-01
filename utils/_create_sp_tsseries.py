
def _create_sp_tsseries():
    nan = np.nan

    # nan-based
    arr = np.arange(15, dtype=np.float64)
    arr[7:12] = nan
    arr[-1:] = nan

    date_index = bdate_range("1/1/2011", periods=len(arr))
    bseries = Series(SparseArray(arr, kind="block"), index=date_index)
    bseries.name = "btsseries"
    return bseries

