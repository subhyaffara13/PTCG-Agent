
def im2col(
    input: Tensor,
    kernel_size: list[int],
    dilation: list[int],
    padding: list[int],
    stride: list[int],
) -> Tensor:
    torch._check(len(kernel_size) == 2, lambda: "im2col(): only 2D kernel supported")
    torch._check(len(dilation) == 2, lambda: "im2col(): only 2D dilation supported")
    torch._check(len(padding) == 2, lambda: "im2col(): only 2D padding supported")
    torch._check(len(stride) == 2, lambda: "im2col(): only 2D stride supported")

    def check_positive(param, param_name, strict=True):
        cond = all(p > 0 for p in param) if strict else all(p >= 0 for p in param)
        torch._check(
            cond, lambda: f"{param_name} should be greater than zero, but got {param}"
        )

    check_positive(kernel_size, "kernel_size")
    check_positive(dilation, "dilation")
    check_positive(dilation, "padding", strict=False)
    check_positive(stride, "stride")

    shape = input.shape
    ndim = len(shape)
    torch._check(
        ndim in (3, 4) and all(d != 0 for d in shape[-3:]),
        lambda: "Expected 3D or 4D (batch mode) tensor for input with possible 0 batch size "
        f"and non-zero dimensions, but got: {tuple(shape)}",
    )
    output_size = tuple(
        1 + (out + 2 * pad - dil * (ker - 1) - 1) // st
        for out, pad, dil, ker, st in zip(
            shape[-2:], padding, dilation, kernel_size, stride
        )
    )
    torch._check(
        all(c > 0 for c in output_size),
        lambda: f"Given an input with spatial size {tuple(shape[-2:])}, "
        f"kernel_size={kernel_size}, dilation={dilation}, "
        f"padding={padding}, stride={stride}, "
        "the calculated shape of the array of sliding blocks "
        f"is {output_size}, but its components must be at least one.",
    )
    batched_input = ndim == 4
    if not batched_input:
        input = input.unsqueeze(0)

    batch_dim, channel_dim, input_h, input_w = input.shape

    stride_h, stride_w = stride
    padding_h, padding_w = padding
    dilation_h, dilation_w = dilation
    kernel_h, kernel_w = kernel_size

    blocks_row_indices = _im2col_col2im_indices_along_dim(
        input_h, kernel_h, dilation_h, padding_h, stride_h, input.device
    )
    blocks_col_indices = _im2col_col2im_indices_along_dim(
        input_w, kernel_w, dilation_w, padding_w, stride_w, input.device
    )

    # Note that F.pad takes (padding_left, padding_right, padding_top, padding_bottom)
    # ugh
    padded_input = F.pad(input, (padding_w, padding_w, padding_h, padding_h))

    blocks_row_indices = blocks_row_indices.unsqueeze(-1).unsqueeze(-1)
    output = padded_input[:, :, blocks_row_indices, blocks_col_indices]
    output = output.permute(0, 1, 2, 4, 3, 5)
    num_blocks_row = blocks_row_indices.size(1)
    num_blocks_col = blocks_col_indices.size(1)
    output = output.reshape(
        batch_dim, channel_dim * kernel_h * kernel_w, num_blocks_row * num_blocks_col
    )

    if not batched_input:
        output = output.squeeze(0)
    return output


def im2col(g: jit_utils.GraphContext, input, kernel_size, dilation, padding, stride):
    # Input is always 4-D tensor (N, C, H, W)
    # All other args are int[2]

    input_h = size(g, input, g.op("Constant", value_t=torch.tensor(2)))
    input_w = size(g, input, g.op("Constant", value_t=torch.tensor(3)))

    stride_h, stride_w = stride[0], stride[1]
    padding_h, padding_w = padding[0], padding[1]
    dilation_h, dilation_w = dilation[0], dilation[1]
    kernel_h, kernel_w = kernel_size[0], kernel_size[1]

    blocks_row_indices = _get_im2col_indices_along_dim(
        g, input_h, kernel_h, dilation_h, padding_h, stride_h
    )
    blocks_col_indices = _get_im2col_indices_along_dim(
        g, input_w, kernel_w, dilation_w, padding_w, stride_w
    )

    output_shape = _get_im2col_output_shape(g, input, kernel_h, kernel_w)
    padded_input = _get_im2col_padded_input(g, input, padding_h, padding_w)

    # For a 4D matrix of size (1, 1, 3, 3) as below with kernel_size=2, stride=1, and dilation=1
    # [[[[1., 2., 3.,],
    #    [4., 5., 6.,],
    #    [7., 8., 9.,]]]]
    # First gather indices along rows (dim=2) with blocks_row_indices = [[0,1], [1,2]] to get:
    # [[[[[1., 2., 3.],
    #     [4., 5., 6.]],
    #    [[4., 5., 6.],
    #     [7., 8., 9.]]]]]
    # And then gather along cols (dim=4) with blocks_row_indices = [[0,1], [1,2]] to get:
    # [[[[[[1., 2.],
    #      [4., 5.]],
    #     [[2., 3.],
    #      [5., 6]]],
    #    [[[4., 5.],
    #      [7., 8.]],
    #     [[5., 6.],
    #      [8., 9.]]]]]]
    # Transpose dims 3 (depth) and 4 (rows), and then reshape to output shape (1, 1, 4, 4) to get:
    #  [[[1., 2., 4., 5.],
    #    [2., 3., 5., 6.],
    #    [4., 5., 7., 8.],
    #    [5., 6., 8., 9.]]]
    output = g.op("Gather", padded_input, blocks_row_indices, axis_i=2)
    output = g.op("Gather", output, blocks_col_indices, axis_i=4)
    output = g.op("Transpose", output, perm_i=[0, 1, 2, 4, 3, 5])
    return symbolic_helper._reshape_helper(g, output, output_shape)

