
def get_num_bytes(t: torch.Tensor) -> int:
    """
    Calculates the memory consumption of a tensor.

    Args:
        t (torch.Tensor): The input tensor.

    Returns:
        int: The memory consumption of the tensor in bytes.
    """
    real_numel = 1
    for size, stride in zip(t.shape, t.stride()):
        # For dims with stride=0 (expanded/broadcast), only 1 element accessed
        if not statically_known_true(stride == 0):
            real_numel *= optimization_hint(size, fallback=0)

    return real_numel * t.element_size()


def get_num_bytes(*args: torch.Tensor, num_in_out_args: int = 0) -> int:
    """
    Return the total number of bytes the arguments of tensor type takes.

    For in/out args, tensor sizes are counted twice: once for reading and
    once for writing.

    The first num_in_out_args arguments are in out tensors.
    """
    return sum(
        arg.numel() * arg.element_size() * (1 + int(i < num_in_out_args))
        for i, arg in enumerate(args)
        if isinstance(arg, torch.Tensor)
    )

