
def _pallas_tile_size(
    dim: int, alignment: int, max_tile: int = 1024, is_tpu: bool = False
) -> int:
    """Pick the largest aligned tile size <= max_tile for *dim*.

    If *dim* is already <= alignment the full dimension is used (no tiling
    on this axis).
    """
    if dim == 0:
        # Tile size >= 1 avoids division by zero in JAX's _pad_to_block_dimension
        return alignment if is_tpu else 1

    if is_tpu:
        # On TPU, Mosaic requires block dimensions to perfectly align to hardware
        # registers (128 for inner, 8 for outer). We MUST pad the block spec up to
        # the next alignment boundary (Mosaic handles the OOB masking).
        if dim <= alignment:
            return alignment
        t = min(max_tile, dim)
        # Use ceiling division to ensure the tile covers the dimension or aligns upward
        t = ((t + alignment - 1) // alignment) * alignment
        return t

    if dim <= alignment:
        return dim
    t = min(max_tile, dim)
    t = (t // alignment) * alignment
    return max(alignment, t)

