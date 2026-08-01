
def from_blocked_format(x_mxfp8, scales_unswizzled, blocksize=32):
    # expand scales
    scales = torch.repeat_interleave(scales_unswizzled, blocksize, dim=1)

    # de-scale and convert
    x_f32 = x_mxfp8.to(torch.float) * scales.to(torch.float)
    return x_f32.to(torch.bfloat16)

