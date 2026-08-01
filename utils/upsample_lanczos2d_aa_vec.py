
def upsample_lanczos2d_aa_vec(input, output_size, align_corners, scale_factors):
    osize = upsample_compute_output_size(input.size(), output_size, scale_factors)
    scale_h = get_scale_value(scale_factors, 0)
    scale_w = get_scale_value(scale_factors, 1)
    return torch.ops.aten._upsample_lanczos2d_aa(
        input, osize, align_corners, scale_h, scale_w
    )

