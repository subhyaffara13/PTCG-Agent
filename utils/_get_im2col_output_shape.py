
def _get_im2col_output_shape(g: jit_utils.GraphContext, input, kernel_h, kernel_w):
    batch_dim = size(g, input, g.op("Constant", value_t=torch.tensor(0)))
    channel_dim = size(g, input, g.op("Constant", value_t=torch.tensor(1)))
    channel_unfolded = g.op(
        "Mul", channel_dim, g.op("Constant", value_t=torch.tensor(kernel_h * kernel_w))
    )

    return g.op(
        "Concat",
        symbolic_helper._unsqueeze_helper(g, batch_dim, [0]),
        symbolic_helper._unsqueeze_helper(g, channel_unfolded, [0]),
        g.op("Constant", value_t=torch.tensor([-1])),
        axis_i=0,
    )

