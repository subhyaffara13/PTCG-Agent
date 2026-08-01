
def _pad1d_common(input, padding, *, is_reflection):
    dim_plane = 0
    dim_w = 1
    nbatch = 1

    if input.ndim == 3:
        nbatch = input.size(0)
        dim_w += 1
        dim_plane += 1

    _padding_check_valid_input(input, padding, dim=1)

    pad_l, pad_r = padding

    nplane = input.size(dim_plane)
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
        output_w >= 1,
        lambda: f"input (W: {input_w}) is too small. Calculated output W: {output_w}",
    )

    if input.ndim == 2:
        return input.new_empty((nplane, output_w))
    else:
        return input.new_empty((nbatch, nplane, output_w))

