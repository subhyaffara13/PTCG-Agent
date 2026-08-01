
def meta_pad3d_backward(grad_output, input, padding):
    torch._check(len(padding) == 6, lambda: "padding size is expected to be 6")
    if input.ndim <= 3:
        raise AssertionError(f"input.ndim must be > 3, got {input.ndim}")
    if grad_output.ndim != input.ndim:
        raise AssertionError(
            f"grad_output.ndim must equal input.ndim, got {grad_output.ndim} != {input.ndim}"
        )

    dim_w = 3
    dim_h = 2
    dim_d = 1

    if input.ndim == 5:
        dim_w += 1
        dim_h += 1
        dim_d += 1

    pad_l, pad_r, pad_t, pad_b, pad_f, pad_bk = padding

    input_d = input.size(dim_d)
    input_h = input.size(dim_h)
    input_w = input.size(dim_w)
    output_d = input_d + pad_f + pad_bk
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
    torch._check(
        output_d == grad_output.size(dim_d),
        lambda: f"grad_output depth unexpected. Expected: {output_d}, Got: {grad_output.size(dim_d)}",
    )

    return input.new_empty(input.shape)

