
def meta_upsample_bimode2d_aa_backward(
    grad_output,
    output_size,
    input_size,
    align_corners,
    scales_h=None,
    scales_w=None,
):
    full_output_size = upsample_common_check(
        input_size, output_size, num_spatial_dims=2
    )
    torch._check(
        grad_output.ndim == 4,
        lambda: f"Expected grad_output to be a tensor of dimension 4 but got: dimension {grad_output.ndim}",
    )
    for i in range(4):
        torch._check(
            grad_output.shape[i] == full_output_size[i],
            lambda: f"""
Expected grad_output to have the same shape as output; output.size({i}) = {full_output_size[i]}
but got grad_output_size({i}) = {grad_output.size(i)}""",
        )
    return grad_output.new_empty(input_size).to(
        memory_format=utils.suggest_memory_format(grad_output)
    )

