from typing import Optional

def max_unpool2d(
    input: Tensor,
    indices: Tensor,
    kernel_size: BroadcastingList2[int],
    stride: Optional[BroadcastingList2[int]] = None,  # noqa: UP045
    padding: BroadcastingList2[int] = 0,
    output_size: Optional[BroadcastingList2[int]] = None,  # noqa: UP045
) -> Tensor:
    r"""Compute a partial inverse of :class:`MaxPool2d`.

    See :class:`~torch.nn.MaxUnpool2d` for details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            max_unpool2d,
            (input,),
            input,
            indices,
            kernel_size,
            stride=stride,
            padding=padding,
            output_size=output_size,
        )
    kernel_size = _pair(kernel_size)
    if stride is not None:
        _stride = _pair(stride)
    else:
        _stride = kernel_size
    padding = _pair(padding)
    output_size = _unpool_output_size(input, kernel_size, _stride, padding, output_size)
    return torch._C._nn.max_unpool2d(input, indices, output_size)


def max_unpool2d(
    self: TensorLike,
    indices: TensorLike,
    output_size: list[int],
):
    torch._check(
        indices.dtype == torch.int64,
        lambda: f"elements in indices should be type int64 but got: {indices.dtype}",
    )
    torch._check(
        len(output_size) == 2,
        lambda: (
            f"There should be exactly two elements (height, width) in output_size, "
            f"but got {len(output_size)} elements."
        ),
    )

    torch._check(
        self.ndim in (3, 4),
        lambda: (
            f"Input to max_unpooling2d should be a 3d or 4d Tensor, "
            f"but got a tensor with {self.ndim} dimensions."
        ),
    )
    torch._check(
        self.shape == indices.shape,
        lambda: (
            f"Expected shape of indices to be same as that of the input tensor ({self.shape}) "
            f"but got indices tensor with shape: {indices.shape}"
        ),
    )

    for i in range(1, self.ndim):
        torch._check(
            self.size(i) > 0,
            lambda: (
                f"max_unpooling2d(): "
                f"Expected input to have non-zero size for non-batch dimensions, "
                f"but got {self.shape} with dimension {i} being empty."
            ),
        )

    return _max_unpoolnd(self, indices, output_size, 2)

