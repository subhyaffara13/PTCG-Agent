
def _pad1d_backward_common(grad_output, input, padding, *, is_reflection):
    dim_w = 1
    if not is_reflection:
        torch._check(len(padding) == 2, lambda: "padding size is expected to be 2")

    if input.ndim == 3:
        dim_w += 1

    pad_l, pad_r = padding

    input_w = input.size(dim_w)
    output_w = input_w + pad_l + pad_r

    if is_reflection:
        torch._check(
            pad_l < input_w and pad_r < input_w,
            lambda: (
                f"Argument #4: Padding size should be less than the corresponding input dimension, "
                f"but got: padding ({pad_l}, {pad_r}) at dimension {dim_w} of input {input.shape}"
            ),
        )

    torch._check(
        output_w == grad_output.size(dim_w),
        lambda: f"grad_output width unexpected. Expected: {output_w}, Got: {grad_output.size(dim_w)}",
    )

    return input.new_empty(input.shape)

