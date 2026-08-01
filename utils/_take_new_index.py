
def _take_new_index(
    obj: DataFrame, indexer: npt.NDArray[np.intp], new_index: Index
) -> DataFrame: ...


def _take_new_index(
    obj: Series, indexer: npt.NDArray[np.intp], new_index: Index
) -> Series: ...


def _take_new_index(
    obj: DataFrame | Series,
    indexer: npt.NDArray[np.intp],
    new_index: Index,
) -> DataFrame | Series:
    if isinstance(obj, ABCSeries):
        new_values = algos.take_nd(obj._values, indexer)
        return obj._constructor(new_values, index=new_index, name=obj.name)
    elif isinstance(obj, ABCDataFrame):
        new_mgr = obj._mgr.reindex_indexer(new_axis=new_index, indexer=indexer, axis=1)
        return obj._constructor_from_mgr(new_mgr, axes=new_mgr.axes)
    else:
        raise ValueError("'obj' should be either a Series or a DataFrame")

