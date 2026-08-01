
def _adjust_num_blocks_and_indices(
    num_blocks: Tensor,
    indices: Tensor,
    new_num_rows: int,
    new_num_cols: int,
) -> tuple[Tensor, Tensor]:
    indices = indices[:, :, :new_num_rows, :new_num_cols]
    num_blocks = num_blocks[:, :, :new_num_rows]
    num_blocks = torch.where(num_blocks < new_num_cols, num_blocks, new_num_cols)
    num_blocks = torch.sum(indices < num_blocks[:, :, :, None], dim=-1).to(torch.int32)
    return num_blocks, indices

