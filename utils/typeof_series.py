
def typeof_series(val, c) -> SeriesType:
    index = typeof_impl(val.index, c)
    arrty = typeof_impl(val.values, c)
    namety = typeof_impl(val.name, c)
    assert arrty.ndim == 1
    assert arrty.layout == "C"
    return SeriesType(arrty.dtype, index, namety)

