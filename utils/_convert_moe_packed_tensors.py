
def _convert_moe_packed_tensors(
    blocks,
    scales,
    *,
    dtype: torch.dtype = torch.bfloat16,
    rows_per_chunk: int = 32768 * 1024,  # TODO these values are not here by mistake ;)
) -> torch.Tensor:
    """
    Convert the mxfp4 weights again, dequantizing and makes them compatible with the forward
    pass of GPT_OSS.
    """
    import math

    blocks = blocks.to(torch.uint8)
    scales = scales.to(torch.int32) - 127  # TODO that's because 128=2**7

    assert blocks.shape[:-1] == scales.shape, f"{blocks.shape[:-1]=} does not match {scales.shape=}"

    lut = torch.tensor(FP4_VALUES, dtype=dtype, device=blocks.device)

    *prefix_shape, G, B = blocks.shape
    rows_total = math.prod(prefix_shape) * G

    blocks = blocks.reshape(rows_total, B)
    scales = scales.reshape(rows_total, 1)

    out = torch.empty(rows_total, B * 2, dtype=dtype, device=blocks.device)

    for r0 in range(0, rows_total, rows_per_chunk):
        r1 = min(r0 + rows_per_chunk, rows_total)

        blk = blocks[r0:r1]
        exp = scales[r0:r1]
        sub = out[r0:r1]

        # This vector is only used to index into `lut`, but is hugeee in GPU memory so we delete it immediately
        idx_lo = (blk & 0x0F).to(torch.int)
        sub[:, 0::2] = lut[idx_lo]
        del idx_lo

        # This vector is only used to index into `lut`, but is hugeee in GPU memory so we delete it immediately
        idx_hi = (blk >> 4).to(torch.int)
        sub[:, 1::2] = lut[idx_hi]
        del idx_hi

        # Perform op
        torch.ldexp(sub, exp, out=sub)
        del blk, exp, sub

    out = out.reshape(*prefix_shape, G, B * 2).view(*prefix_shape, G * B * 2)

    return out.transpose(1, 2).contiguous()

