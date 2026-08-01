
def _postprocess_for_cut(fac, bins, retbins: bool, original):
    """
    handles post processing for the cut method where
    we combine the index information if the originally passed
    datatype was a series
    """
    if isinstance(original, ABCSeries):
        fac = original._constructor(fac, index=original.index, name=original.name)

    if not retbins:
        return fac

    if isinstance(bins, Index) and is_numeric_dtype(bins.dtype):
        bins = bins._values

    return fac, bins

