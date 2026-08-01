
def is_contiguous(a: TensorLikeType, false_if_dde=False) -> bool:
    """
    Tests whether a tensor is contiguous or not.

    Tensors are contiguous when they have no elements,
    one element, or when they have "nested" strides.
    """
    from torch.fx.experimental.symbolic_shapes import (
        guard_or_false,
        guard_size_oblivious,
    )

    def eval_eager(x):
        return bool(x)

    maybe_guard_or_false = guard_or_false if false_if_dde else eval_eager

    if maybe_guard_or_false(a.numel() < 2):
        return True

    return check_contiguous_sizes_strides(
        a.shape, a.stride(), false_if_dde=false_if_dde
    )


def is_contiguous(func, *args, **kwargs):
    data = _get_data(args[0])
    if data.is_sparse:
        raise ValueError("MaskedTensors with sparse data do not have is_contiguous")
    return func(data, *args[1:], **kwargs)

