
def union_indexes(indexes, sort: bool | lib.NoDefault = True) -> Index:
    """
    Return the union of indexes.

    The behavior of sort and names is not consistent.

    Parameters
    ----------
    indexes : list of Index or list objects
    sort : bool, default True
        Whether the result index should come out sorted or not. NoDefault
        used for deprecation of GH#57335.

    Returns
    -------
    Index
    """
    if len(indexes) == 0:
        raise AssertionError("Must have at least 1 Index to union")
    if len(indexes) == 1:
        result = indexes[0]
        if isinstance(result, list):
            if not sort or sort is lib.no_default:
                result = Index(result)
            else:
                result = Index(sorted(result))
        return result

    indexes, kind = _sanitize_and_check(indexes)

    if kind == "special":
        result = indexes[0]

        num_dtis = 0
        num_dti_tzs = 0
        for idx in indexes:
            if isinstance(idx, DatetimeIndex):
                num_dtis += 1
                if idx.tz is not None:
                    num_dti_tzs += 1
        if num_dti_tzs not in [0, num_dtis]:
            # TODO: this behavior is not tested (so may not be desired),
            #  but is kept in order to keep behavior the same when
            #  deprecating union_many
            # test_frame_from_dict_with_mixed_indexes
            raise TypeError("Cannot join tz-naive with tz-aware DatetimeIndex")

        if num_dtis == len(indexes):
            if sort is lib.no_default:
                sort = True
            result = indexes[0]

        elif num_dtis > 1:
            # If we have mixed timezones, our casting behavior may depend on
            #  the order of indexes, which we don't want.
            sort = False

            # TODO: what about Categorical[dt64]?
            # test_frame_from_dict_with_mixed_indexes
            indexes = [x.astype(object, copy=False) for x in indexes]
            result = indexes[0]

        for other in indexes[1:]:
            result = result.union(other, sort=None if sort else False)
        return result

    elif kind == "array":
        if not all_indexes_same(indexes):
            dtype = find_common_type([idx.dtype for idx in indexes])
            inds = [ind.astype(dtype, copy=False) for ind in indexes]
            index = inds[0].unique()
            other = inds[1].append(inds[2:])
            diff = other[index.get_indexer_for(other) == -1]
            if len(diff):
                index = index.append(diff.unique())
            if sort:
                index = index.sort_values()
        else:
            index = indexes[0]

        name = get_unanimous_names(*indexes)[0]
        if name != index.name:
            index = index.rename(name)
        return index
    elif kind == "list":
        dtypes = [idx.dtype for idx in indexes if isinstance(idx, Index)]
        if dtypes:
            dtype = find_common_type(dtypes)
        else:
            dtype = None
        all_lists = (idx.tolist() if isinstance(idx, Index) else idx for idx in indexes)
        return Index(
            lib.fast_unique_multiple_list_gen(all_lists, sort=bool(sort)),
            dtype=dtype,
        )
    else:
        raise ValueError(f"{kind=} must be 'special', 'array' or 'list'.")

