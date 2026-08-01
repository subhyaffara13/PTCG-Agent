
def _homogenize(
    data, index: Index, dtype: DtypeObj | None
) -> tuple[list[ArrayLike], list[Any]]:
    oindex = None
    homogenized = []
    # if the original array-like in `data` is a Series, keep track of this Series' refs
    refs: list[Any] = []

    for val in data:
        if isinstance(val, (ABCSeries, Index)):
            if dtype is not None:
                val = val.astype(dtype)
            if isinstance(val, ABCSeries) and val.index is not index:
                # Forces alignment. No need to copy data since we
                # are putting it into an ndarray later
                val = val.reindex(index)
            refs.append(val._references)
            val = val._values
        else:
            if isinstance(val, dict):
                # GH#41785 this _should_ be equivalent to (but faster than)
                #  val = Series(val, index=index)._values
                if oindex is None:
                    oindex = index.astype("O")

                if isinstance(index, (DatetimeIndex, TimedeltaIndex)):
                    # see test_constructor_dict_datetime64_index
                    val = dict_compat(val)
                else:
                    # see test_constructor_subclass_dict
                    val = dict(val)

                if not isinstance(index, MultiIndex) and index.hasnans:
                    # GH#63889 Check if dict has missing value keys that need special
                    # handling (i.e. None/np.nan/pd.NA might no longer be matched
                    # when using fast_multiget with processed object index values)
                    from pandas import Series

                    val = Series(val).reindex(index)._values
                else:
                    # Fast path: use lib.fast_multiget for dicts without missing keys
                    val = lib.fast_multiget(val, oindex._values, default=np.nan)

            val = sanitize_array(val, index, dtype=dtype, copy=False)
            com.require_length_match(val, index)
            refs.append(None)

        homogenized.append(val)

    return homogenized, refs

