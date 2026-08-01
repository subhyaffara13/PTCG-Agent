
def eval_is_non_overlapping_and_dense(
    sizes: Sequence[int], strides: Sequence[int]
) -> int:
    return int(guard_bool(_eval_is_non_overlapping_and_dense(sizes, strides)))

