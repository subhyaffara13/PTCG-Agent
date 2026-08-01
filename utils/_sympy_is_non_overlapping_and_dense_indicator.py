
def _sympy_is_non_overlapping_and_dense_indicator(
    sizes: list[sympy.Basic], strides: list[sympy.Basic]
) -> sympy.Basic:
    from torch.utils._sympy.functions import IsNonOverlappingAndDenseIndicator

    return IsNonOverlappingAndDenseIndicator(*sizes, *strides)

