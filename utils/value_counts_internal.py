
def value_counts_internal(
    values,
    sort: bool = True,
    ascending: bool = False,
    normalize: bool = False,
    bins=None,
    dropna: bool = True,
) -> Series:
    from pandas import (
        DatetimeIndex,
        Index,
        Series,
        TimedeltaIndex,
    )

    index_name = getattr(values, "name", None)
    name = "proportion" if normalize else "count"

    if bins is not None:
        from pandas.core.reshape.tile import cut

        if isinstance(values, Series):
            values = values._values

        try:
            ii = cut(values, bins, include_lowest=True)
        except TypeError as err:
            raise TypeError("bins argument only works with numeric data.") from err

        # count, remove nulls (from the index), and but the bins
        result = ii.value_counts(dropna=dropna)
        result.name = name
        result = result[result.index.notna()]
        result.index = result.index.astype("interval")
        result = result.sort_index()

        # if we are dropna and we have NO values
        if dropna and (result._values == 0).all():
            result = result.iloc[0:0]

        # normalizing is by len of all (regardless of dropna)
        normalize_denominator = len(ii)

    else:
        normalize_denominator = None
        if is_extension_array_dtype(values):
            # handle Categorical and sparse,
            result = Series(values, copy=False)._values.value_counts(dropna=dropna)
            result.name = name
            result.index.name = index_name

        elif isinstance(values, ABCMultiIndex):
            # GH49558
            levels = list(range(values.nlevels))
            result = (
                Series(index=values, name=name)
                .groupby(level=levels, dropna=dropna)
                .size()
            )
            result.index.names = values.names

        else:
            values = _ensure_arraylike(values, func_name="value_counts")
            keys, counts, _ = value_counts_arraylike(values, dropna)
            if keys.dtype == np.float16:
                keys = keys.astype(np.float32)

            # Starting in 3.0, we no longer perform dtype inference on the
            #  Index object we construct here, xref GH#56161
            idx = Index(keys, dtype=keys.dtype, name=index_name, copy=False)

            if (
                not sort
                and isinstance(values, (DatetimeIndex, TimedeltaIndex))
                and idx.equals(values)
                and values.inferred_freq is not None
            ):
                # Preserve freq of original index
                idx.freq = values.inferred_freq  # type: ignore[attr-defined]

            result = Series(counts, index=idx, name=name, copy=False)

    if sort:
        result = result.sort_values(ascending=ascending, kind="stable")

    if normalize:
        if normalize_denominator is not None:
            result = result / normalize_denominator
        else:
            result = result / result.sum()

    return result

