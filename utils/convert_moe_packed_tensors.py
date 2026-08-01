
def convert_moe_packed_tensors(
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
    # Since the intermediate ops requite A LOT of memory, in very constrained device_map="auto" settings
    # it may OOM, hence this wrapper and move back to cpu if needed
    # torch statistics are not accurate enough to estimate if we will have enough memory due to fragmentation and
    # in-place operation on non-contiguous tensors (may sometimes require more temporary copies)
    try:
        return _convert_moe_packed_tensors(blocks, scales, dtype=dtype, rows_per_chunk=rows_per_chunk)
    # In the case of OOM due to very tight device_map, we convert and return on cpu - it will then be put back on correct
    # devide with the accelerate dispatch (doing it right away may still lead to OOM, but more memory is available later)
    except torch.OutOfMemoryError:
        blocks = blocks.to("cpu")
        scales = scales.to("cpu")
        return _convert_moe_packed_tensors(blocks, scales, dtype=dtype, rows_per_chunk=rows_per_chunk)

