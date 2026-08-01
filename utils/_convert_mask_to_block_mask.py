
def _convert_mask_to_block_mask(
    mask: Tensor,
    Q_BLOCK_SIZE: int = _DEFAULT_SPARSE_BLOCK_SIZE,
    KV_BLOCK_SIZE: int = _DEFAULT_SPARSE_BLOCK_SIZE,
    separate_full_blocks: bool = False,
) -> tuple[Tensor, Tensor | None]:
    if mask.dtype != torch.bool:
        raise AssertionError(f"mask.dtype must be torch.bool, got {mask.dtype}")
    mask = _broadcast_to_dim(mask, 4)

    def padding_needed_for_multiple(x, multiple):
        return _round_up_to_multiple(x, multiple) - x

    mask = torch.nn.functional.pad(
        mask,
        (
            0,
            padding_needed_for_multiple(mask.shape[-1], KV_BLOCK_SIZE),
            0,
            padding_needed_for_multiple(mask.shape[-2], Q_BLOCK_SIZE),
        ),
    )
    B, H, Q, KV = mask.shape
    if Q % Q_BLOCK_SIZE != 0:
        raise AssertionError(
            f"Q ({Q}) must be divisible by Q_BLOCK_SIZE ({Q_BLOCK_SIZE})"
        )
    if KV % KV_BLOCK_SIZE != 0:
        raise AssertionError(
            f"KV ({KV}) must be divisible by KV_BLOCK_SIZE ({KV_BLOCK_SIZE})"
        )
    mask = mask.view(
        B, H, Q // Q_BLOCK_SIZE, Q_BLOCK_SIZE, KV // KV_BLOCK_SIZE, KV_BLOCK_SIZE
    )  # [B, H, Q//Q_BLOCK_SIZE, Q_BLOCK_SIZE, KV//KV_BLOCK_SIZE, KV_BLOCK_SIZE]
    mask = mask.permute(
        0, 1, 2, 4, 3, 5
    )  # [B, H, Q//Q_BLOCK_SIZE, KV//KV_BLOCK_SIZE, Q_BLOCK_SIZE, KV_BLOCK_SIZE]
    mask_block_sum = mask.sum(
        dim=[-2, -1]
    )  # [B, H, Q//Q_BLOCK_SIZE, KV//KV_BLOCK_SIZE]
    if separate_full_blocks:
        full_block_sum = Q_BLOCK_SIZE * KV_BLOCK_SIZE
        full_blocks = mask_block_sum == full_block_sum
        partial_blocks = (mask_block_sum > 0) & (mask_block_sum < full_block_sum)
        partial_blocks = partial_blocks.to(dtype=torch.int8)
        full_blocks = full_blocks.to(dtype=torch.int8)
        return partial_blocks, full_blocks
    else:
        partial_blocks = mask_block_sum > 0
        partial_blocks = partial_blocks.to(dtype=torch.int8)
        return partial_blocks, None

