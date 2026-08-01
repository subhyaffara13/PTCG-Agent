
def get_alignments(torch_dtype: torch.dtype) -> list[int]:
    """
    Returns all possible valid CUTLASS alignments in terms of the number of elements for a given dtype.
    CUTLASS gemm / conv SM80 APIs support 16 bytes max alignment, and 2 bytes min alignment.
    """

    if torch_dtype in (torch.half, torch.bfloat16):
        return [8, 4, 2, 1]
    elif torch_dtype == torch.float:
        return [4, 2, 1]
    elif torch_dtype in (
        torch.uint8,
        torch.int8,
        torch.float8_e4m3fn,
        torch.float8_e5m2,
    ):
        return [16, 8, 4, 2]
    elif torch_dtype == torch.int32:
        return [4, 2, 1]
    else:
        raise NotImplementedError(f"unsupported {torch_dtype=} for alignments")

