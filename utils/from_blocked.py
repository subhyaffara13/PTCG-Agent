
def from_blocked(input, input_scales, blocksize) -> torch.Tensor:
    # Matrix is in a 128x4 pattern, internally blocked as 32x4x4 nonsense.
    # Output should be [input.size(0, input.size(1) // blocksize] scales
    output_scales = torch.zeros(
        (input.size(0), input.size(1) // blocksize),
        device=input.device,
        dtype=input_scales.dtype,
    )

    # Swizzled scales are padded to tiles of 128x4, we need to replicate how that padding
    # happened for offset purposes.
    # There are K//blocksize scales, padded to groups of 4.
    num_col_tiles = ceil_div(ceil_div(input.size(1), blocksize), 4)

    # (Very) slow reference implementation using horrifying loops.
    for i in range(input.size(0)):
        for j in range(input.size(1) // blocksize):
            # which 128x4 tile of scaling factors am I in
            scale_tile_h = i // 128
            scale_tile_w = j // 4

            # There are (padded) input_scales.size(1) // 4 tiles along the w dim.
            # So offset is 512 * (h_tile * tiles_per_row + tile_in_row)
            tile_offset = 512 * (scale_tile_h * num_col_tiles + scale_tile_w)

            # indices within the tile - use nomenclature directly from cublas docs
            outer = i % 128  # "outer" in cublas docs
            inner = j % 4    # "inner" in cublas docs

            # Note: "offset" is given in terms of bytes, in cublas docs, but our scales are e8m0,
            #       anyway, and so 1B == 1 value => use offset directly.
            # Formula directly from cublas docs in 3.1.4.3.2
            offset = tile_offset + (outer % 32) * 16 + (outer // 32) * 4 + inner

            output_scales[i, j] = input_scales[offset]

    return output_scales

