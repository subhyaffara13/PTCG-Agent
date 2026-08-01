
def _upsample_linear_vec(input, output_size, align_corners, scale_factors):
    osize = upsample_compute_output_size(input.size(), output_size, scale_factors)
    scales = scale_factors if scale_factors else [None] * len(osize)
    return _upsample_linear(input, osize, align_corners, scales)

