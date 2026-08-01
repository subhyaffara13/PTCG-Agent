
def get_vision_cu_seqlens(grid_thw: torch.Tensor, kwargs: dict | None = None) -> torch.Tensor:
    """Get cumulative sequence lengths from vision grid info, or pop from `kwargs` if precomputed.

    Args:
        grid_thw: `(num_images_or_videos, 3)` — temporal, height, width per entry.
        kwargs: optional caller kwargs — if it contains `"cu_seqlens"` it is popped and returned.

    Returns:
        `cu_seqlens`: `(total_patches + 1,)` int32 cumulative sequence boundaries.
    """
    if kwargs is not None and (cu_seqlens := kwargs.pop("cu_seqlens", None)) is not None:
        return cu_seqlens
    cu_seqlens = torch.repeat_interleave(grid_thw[:, 1] * grid_thw[:, 2], grid_thw[:, 0]).cumsum(
        dim=0, dtype=grid_thw.dtype if torch.jit.is_tracing() else torch.int32
    )
    return F.pad(cu_seqlens, (1, 0), value=0)

