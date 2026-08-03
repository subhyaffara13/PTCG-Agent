from typing import Callable

def _get_result(
    objs: list[Series | DataFrame],
    is_series: bool,
    bm_axis: AxisInt,
    ignore_index: bool,
    intersect: bool,
    sort: bool | lib.NoDefault,
    keys: Iterable[Hashable] | None,
    levels,
    verify_integrity: bool,
    names: list[HashableT] | None,
    axis: AxisInt,
):
    cons: Callable[..., DataFrame | Series]
    sample: DataFrame | Series

    # series only
    if is_series:
        sample = cast("Series", objs[0])

        # stack blocks
        if bm_axis == 0:
            name = com.consensus_name_attr(objs)
            cons = sample._constructor

            arrs = [ser._values for ser in objs]

            res = concat_compat(arrs, axis=0)

            if ignore_index:
                new_index: Index = default_index(len(res))
            else:
                new_index = _get_concat_axis_series(
                    objs,
                    ignore_index,
                    bm_axis,
                    keys,
                    levels,
                    verify_integrity,
                    names,
                )

            mgr = type(sample._mgr).from_array(res, index=new_index)

            result = sample._constructor_from_mgr(mgr, axes=mgr.axes)
            result._name = name
            return result.__finalize__(
                types.SimpleNamespace(input_objs=objs, objs=objs), method="concat"
            )

        # combine as columns in a frame
        else:
            data = dict(enumerate(objs))

            # GH28330 Preserves subclassed objects through concat
            cons = sample._constructor_expanddim

            index = get_objs_combined_axis(
                objs,
                axis=objs[0]._get_block_manager_axis(0),
                intersect=intersect,
                sort=sort,
            )
            columns = _get_concat_axis_series(
                objs, ignore_index, bm_axis, keys, levels, verify_integrity, names
            )
            df = cons(data, index=index, copy=False)
            df.columns = columns
            return df.__finalize__(
                types.SimpleNamespace(input_objs=objs, objs=objs), method="concat"
            )

    # combine block managers
    else:
        sample = cast("DataFrame", objs[0])

        mgrs_indexers = []
        result_axes = new_axes(
            objs,
            bm_axis,
            intersect,
            sort,
            keys,
            names,
            axis,
            levels,
            verify_integrity,
            ignore_index,
        )
        for obj in objs:
            indexers = {}
            for ax, new_labels in enumerate(result_axes):
                # ::-1 to convert BlockManager ax to DataFrame ax
                if ax == bm_axis:
                    # Suppress reindexing on concat axis
                    continue

                # 1-ax to convert BlockManager axis to DataFrame axis
                obj_labels = obj.axes[1 - ax]
                if not new_labels.equals(obj_labels):
                    indexers[ax] = obj_labels.get_indexer(new_labels)

            mgrs_indexers.append((obj._mgr, indexers))

        new_data = concatenate_managers(
            mgrs_indexers, result_axes, concat_axis=bm_axis, copy=False
        )

        out = sample._constructor_from_mgr(new_data, axes=new_data.axes)
        return out.__finalize__(
            types.SimpleNamespace(input_objs=objs, objs=objs), method="concat"
        )

