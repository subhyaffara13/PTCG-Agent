
def meta_upsample_bimode2d_aa(
    input,
    output_size,
    align_corners,
    scales_h=None,
    scales_w=None,
):
    full_output_size = upsample_common_check(
        input.size(), output_size, num_spatial_dims=2
    )
    torch._check(
        input.numel() != 0 or all(size > 0 for size in input.size()[1:]),
        lambda: f"Non-empty 4D data tensor expected but got a tensor with sizes {input.size()}",
    )
    return input.new_empty(full_output_size).to(
        memory_format=utils.suggest_memory_format(input)
    )

