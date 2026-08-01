
def _get_im2col_padded_input(g: jit_utils.GraphContext, input, padding_h, padding_w):
    # Input is always 4-D tensor (N, C, H, W)
    # Padding tensor has the following format: (padding_h, padding_w)
    # Reshape the padding to follow ONNX format: (dim1_begin, dim2_begin,...,dim1_end, dim2_end,...)
    pad = g.op("Constant", value_t=torch.LongTensor([0, 0, padding_h, padding_w] * 2))
    return g.op("Pad", input, pad)

