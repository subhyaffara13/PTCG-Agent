
def _bn_ok_dtype(dtype: DtypeObj, name: str) -> bool:
    # Bottleneck chokes on datetime64, PeriodDtype (or and EA)
    if dtype != object and not needs_i8_conversion(dtype):
        # GH 42878
        # Bottleneck uses naive summation leading to O(n) loss of precision
        # unlike numpy which implements pairwise summation, which has O(log(n)) loss
        # crossref: https://github.com/pydata/bottleneck/issues/379

        # GH 15507
        # bottleneck does not properly upcast during the sum
        # so can overflow

        # GH 9422
        # further we also want to preserve NaN when all elements
        # are NaN, unlike bottleneck/numpy which consider this
        # to be 0
        return name not in ["nansum", "nanprod", "nanmean"]
    return False

