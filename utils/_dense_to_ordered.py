
def _dense_to_ordered(dense_mask: Tensor) -> tuple[Tensor, Tensor]:
    dense_mask = dense_mask.to(dtype=torch.int32)
    num_blocks_in_row = dense_mask.sum(dim=-1)
    col_indices = torch.argsort(dense_mask, dim=-1, descending=True, stable=True)
    return (
        num_blocks_in_row.to(torch.int32, memory_format=torch.contiguous_format),
        col_indices.to(torch.int32, memory_format=torch.contiguous_format),
    )

