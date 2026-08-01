
def complex_conv(fn, input_size, weight, grad_output, stride, padding, dilation, groups):
    # conv(W, x, b) = conv(Wr, xr, br) - conv(Wi, xi, 0) + i(conv(Wi, xr, bi) + conv(Wr, xi, 0))
    # a = conv(Wr, xr, br),
    # b = conv(Wi, xi, 0),
    # c = conv(Wr + Wi, xr + xi, br + bi)
    # conv(W, x, b) = a - b + i(c - a - b)

    grad_output_ = torch.view_as_real(grad_output)
    grad_output_r = grad_output_[..., 0]
    grad_output_i = grad_output_[..., 1]

    weight_ = torch.view_as_real(weight)
    weight_r = weight_[..., 0]
    weight_i = weight_[..., 1]

    a = fn(input_size, weight_r, grad_output_r, stride, padding, dilation, groups)
    b = fn(input_size, weight_i, grad_output_i, stride, padding, dilation, groups)
    c = fn(input_size, weight_r + weight_i, grad_output_r + grad_output_i, stride, padding, dilation, groups)

    return (a - b) + 1j * (c - a - b)

