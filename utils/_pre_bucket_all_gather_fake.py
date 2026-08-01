
def _pre_bucket_all_gather_fake(
    ag_ins: list[torch.Tensor],
    group_size: int,
    group_name: str,
    dtype: torch.dtype,  # type: ignore[name-defined]
    out_dtype_ints: list[int],
    rank: int,
    foreach_group_indices: list[int] | None = None,
) -> torch.Tensor:
    out_dtypes = [_ALL_DTYPES[d] for d in out_dtype_ints]
    ins_split_sizes_bytes = [
        ag_in.numel() * out_dtype.itemsize
        for ag_in, out_dtype in zip(ag_ins, out_dtypes, strict=True)
    ]
    bucket_dtype_size_bytes = dtype.itemsize
    ins_split_sizes = [
        _bytes // bucket_dtype_size_bytes for _bytes in ins_split_sizes_bytes
    ]
    ag_input_numel = sum(ins_split_sizes)
    device = ag_ins[0].device
    new_ag_out = torch.empty(ag_input_numel * group_size, dtype=dtype, device=device)
    return new_ag_out

