
def _eval_is_non_overlapping_and_dense_flat(*args: int) -> int:
    # Guard code strings print IsNonOverlappingAndDenseIndicator with flat args
    # (s0, s1, ..., stride0, stride1, ...) but eval_is_non_overlapping_and_dense
    # expects two sequences (sizes, strides). This wrapper bridges the gap.
    dim = len(args) // 2
    return eval_is_non_overlapping_and_dense(list(args[:dim]), list(args[dim:]))

