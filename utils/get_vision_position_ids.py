
def get_vision_position_ids(
    grid_thw: torch.Tensor, spatial_merge_size: int | torch.Tensor, kwargs: dict | None = None
) -> torch.Tensor:
    """Get (row, col) position IDs for vision rotary embeddings, or pop from `kwargs` if precomputed.

    Args:
        grid_thw: `(num_images_or_videos, 3)`
        spatial_merge_size: merge block size — either a single `int` (same for all images)
            or a `(num_images_or_videos,)` tensor (per-image).
        kwargs: optional caller kwargs — if it contains `"position_ids"` it is popped and returned.

    Returns:
        `position_ids`: `(total_tokens, 2)` long — (row, col) position per token.
    """
    if kwargs is not None and (position_ids := kwargs.pop("position_ids", None)) is not None:
        return position_ids
    device = grid_thw.device
    if isinstance(spatial_merge_size, int):
        spatial_merge_size = torch.tensor([spatial_merge_size], device=device).expand(len(grid_thw))

    position_ids = []
    for (t, h, w), merge_size in zip(grid_thw.tolist(), spatial_merge_size.tolist()):
        t, h, w, merge_size = int(t), int(h), int(w), int(merge_size)
        hpos_ids = torch.arange(h, device=device).unsqueeze(1).expand(-1, w)
        hpos_ids = hpos_ids.reshape(h // merge_size, merge_size, w // merge_size, merge_size).transpose(1, 2).flatten()

        wpos_ids = torch.arange(w, device=device).unsqueeze(0).expand(h, -1)
        wpos_ids = wpos_ids.reshape(h // merge_size, merge_size, w // merge_size, merge_size).transpose(1, 2).flatten()
        position_ids.append(torch.stack([hpos_ids, wpos_ids], dim=-1).repeat(t, 1))

    return torch.cat(position_ids, dim=0)

