
def _unstack_frame(
    obj: DataFrame, level, fill_value=None, sort: bool = True
) -> DataFrame:
    assert isinstance(obj.index, MultiIndex)  # checked by caller
    unstacker = _Unstacker(
        obj.index, level=level, constructor=obj._constructor, sort=sort
    )

    if not obj._can_fast_transpose:
        mgr = obj._mgr.unstack(unstacker, fill_value=fill_value)
        return obj._constructor_from_mgr(mgr, axes=mgr.axes)
    else:
        return unstacker.get_result(
            obj, value_columns=obj.columns, fill_value=fill_value
        )

