
def _get_im2col_indices_along_dim(
    g: jit_utils.GraphContext, input_d, kernel_size_d, dilation_d, padding_d, stride_d
):
    # Input is always 4-D (N, C, H, W)
    # Calculate indices of sliding blocks along spatial dimension
    # Slide kernel over input each dim d:
    # each dimension d ranges from 0 to input[d]+2xpadding[d]-dilation[d]x(kernel_size[d]-1)
    # with steps = stride

    blocks_d = g.op(
        "Add", input_d, g.op("Constant", value_t=torch.tensor(padding_d * 2))
    )
    blocks_d = g.op(
        "Sub",
        blocks_d,
        g.op("Constant", value_t=torch.tensor(dilation_d * (kernel_size_d - 1))),
    )

    # Stride kernel over input and find starting indices along dim d
    blocks_d_indices = g.op(
        "Range",
        g.op("Constant", value_t=torch.tensor(0)),
        blocks_d,
        g.op("Constant", value_t=torch.tensor(stride_d)),
    )

    # Apply dilation on kernel and find its indices along dim d
    kernel_grid = torch.arange(0, kernel_size_d * dilation_d, dilation_d)
    kernel_grid = g.op("Constant", value_t=kernel_grid.unsqueeze(0))

    # Broadcast and add kernel staring positions (indices) with
    # kernel_grid along dim d, to get block indices along dim d
    blocks_d_indices = symbolic_helper._unsqueeze_helper(
        g, blocks_d_indices, [0]
    )  # Reshape to [1, -1]
    kernel_mask = symbolic_helper._reshape_helper(
        g, kernel_grid, g.op("Constant", value_t=torch.tensor([-1, 1]))
    )
    block_mask = g.op("Add", blocks_d_indices, kernel_mask)

    return block_mask

