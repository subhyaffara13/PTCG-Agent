
def meta_pad2d_backward(grad_output, self, padding):
    dim_w = 2
    dim_h = 1
    dim_plane = 0

    self_shape = self.shape
    if self.dim() == 4:
        dim_w += 1
        dim_h += 1
        dim_plane += 1

    pad_l, pad_r, pad_t, pad_b = padding

    input_h = self_shape[dim_h]
    input_w = self_shape[dim_w]
    output_h = input_h + pad_t + pad_b
    output_w = input_w + pad_l + pad_r

    torch._check(
        output_w == grad_output.size(dim_w),
        lambda: f"grad_output width unexpected. Expected: {output_w}, Got: {grad_output.size(dim_w)}",
    )
    torch._check(
        output_h == grad_output.size(dim_h),
        lambda: f"grad_output height unexpected. Expected: {output_h}, Got: {grad_output.size(dim_h)}",
    )
    return self.new_empty(self.shape)

