
def is_channels_last_contiguous_2d(a: Tensor, false_if_dde=False) -> bool:
    # NHWC or not channels last 2D contiguous
    if a.ndim != 4:
        return False

    from torch.fx.experimental.symbolic_shapes import guard_or_false, guard_or_true

    def eval_eager(x):
        return bool(x)

    maybe_guard_or_false = guard_or_false if false_if_dde else eval_eager
    maybe_guard_or_true = guard_or_true if false_if_dde else eval_eager

    expected_stride = 1
    for idx in (1, 3, 2, 0):
        length = a.shape[idx]
        if maybe_guard_or_false(length == 1):
            continue

        stride = a.stride()[idx]
        if maybe_guard_or_true(stride != expected_stride):
            return False

        expected_stride *= length

    return True

