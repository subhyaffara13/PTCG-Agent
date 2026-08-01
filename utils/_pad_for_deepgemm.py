
def _pad_for_deepgemm(x: torch.Tensor, sorted_to_padded: torch.Tensor, total_padded_rows: int) -> torch.Tensor:
    """Pad a sorted tensor into the TMA-aligned contiguous layout."""
    padded = torch.empty(total_padded_rows, *x.shape[1:], device=x.device, dtype=x.dtype)
    padded[sorted_to_padded] = x
    return padded

