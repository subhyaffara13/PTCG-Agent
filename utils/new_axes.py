
def new_axes(
    objs: list[Series | DataFrame],
    bm_axis: AxisInt,
    intersect: bool,
    sort: bool | lib.NoDefault,
    keys: Iterable[Hashable] | None,
    names: list[HashableT] | None,
    axis: AxisInt,
    levels,
    verify_integrity: bool,
    ignore_index: bool,
) -> list[Index]:
    """Return the new [index, column] result for concat."""
    return [
        _get_concat_axis_dataframe(
            objs,
            axis,
            ignore_index,
            keys,
            names,
            levels,
            verify_integrity,
        )
        if i == bm_axis
        else get_objs_combined_axis(
            objs,
            axis=objs[0]._get_block_manager_axis(i),
            intersect=intersect,
            sort=sort,
        )
        for i in range(2)
    ]

