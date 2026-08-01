
def _get_dim_chunked_size(
    chunk: torch.Tensor, unchunked_size: torch.Size, dim: int
) -> torch.Size:
    if chunk.numel() > 0:
        return chunk.size()
    # For 0 numel, we need to preserve nonzero-sized dims for DTensor APIs
    # pyrefly: ignore [bad-return]
    return unchunked_size[:dim] + torch.Size([0]) + unchunked_size[dim + 1 :]

