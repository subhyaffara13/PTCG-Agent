from typing import Optional

def lp_pool1d(
    input: Tensor,
    norm_type: int | float,
    kernel_size: int,
    stride: Optional[BroadcastingList1[int]] = None,  # noqa: UP045
    ceil_mode: bool = False,
) -> Tensor:
    r"""Apply a 1D power-average pooling over an input signal composed of several input planes.

    If the sum of all inputs to the power of `p` is
    zero, the gradient is set to zero as well.

    When ``ceil_mode`` is ``True``, sliding windows may go off-bounds if they start within the left
    padding or the input. Sliding windows that would start in the right padded region are ignored.

    See :class:`~torch.nn.LPPool1d` for details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            lp_pool1d,
            (input,),
            input,
            norm_type,
            kernel_size,
            stride=stride,
            ceil_mode=ceil_mode,
        )
    if stride is not None:
        out = avg_pool1d(input.pow(norm_type), kernel_size, stride, 0, ceil_mode)
    else:
        out = avg_pool1d(
            input.pow(norm_type), kernel_size, padding=0, ceil_mode=ceil_mode
        )

    return (
        (torch.sign(out) * relu(torch.abs(out))).mul(kernel_size).pow(1.0 / norm_type)
    )

