
def max_unpool3d(
    input: Tensor,
    indices: Tensor,
    kernel_size: BroadcastingList3[int],
    stride: Optional[BroadcastingList3[int]] = None,  # noqa: UP045
    padding: BroadcastingList3[int] = 0,
    output_size: Optional[BroadcastingList3[int]] = None,  # noqa: UP045
) -> Tensor:
    r"""Compute a partial inverse of :class:`MaxPool3d`.

    See :class:`~torch.nn.MaxUnpool3d` for details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            max_unpool3d,
            (input,),
            input,
            indices,
            kernel_size,
            stride=stride,
            padding=padding,
            output_size=output_size,
        )
    kernel_size = _triple(kernel_size)
    if stride is not None:
        _stride = _triple(stride)
    else:
        _stride = kernel_size
    padding = _triple(padding)
    output_size = _unpool_output_size(input, kernel_size, _stride, padding, output_size)
    return torch._C._nn.max_unpool3d(input, indices, output_size, _stride, padding)


def max_unpool3d(
    input: TensorLike,
    indices: TensorLike,
    output_size: list[int],
    stride: list[int],
    padding: list[int],
):
    torch._check(
        indices.dtype == torch.int64, lambda: "elements in indices should be type int64"
    )
    torch._check(
        input.ndim in (4, 5),
        lambda: f"Input to max_unpooling3d should be a 4d or 5d Tensor, but got a tensor with {input.ndim} dimensions.",
    )
    torch._check(
        len(output_size) == 3,
        lambda: (
            f"There should be exactly three elements (depth, height, width) in output_size, "
            f"but got {len(output_size)} elements."
        ),
    )
    torch._check(
        len(stride) == 3,
        lambda: f"There should be exactly three elements (depth, height, width) in stride, but got: {len(stride)} elements.",
    )
    torch._check(
        len(padding) == 3,
        lambda: f"There should be exactly three elements (depth, height, width) in padding, but got: {len(padding)} elements.",
    )
    torch._check(
        input.shape == indices.shape,
        lambda: (
            f"Expected shape of indices to be same as that of the input tensor ({input.shape}) "
            f"but got indices tensor with shape: {indices.shape}"
        ),
    )

    for i in range(1, input.ndim):
        torch._check(
            input.size(i) > 0,
            lambda: (
                f"max_unpooling3d(): "
                f"Expected input to have non-zero size for non-batch dimensions, "
                f"but got {input.shape} with dimension {i} being empty."
            ),
        )

    torch._check(
        stride[0] > 0 and stride[1] > 0 and stride[2] > 0,
        lambda: f"strides should be greater than zero, but got stride: {stride}",
    )

    return _max_unpoolnd(input, indices, output_size, 3)

