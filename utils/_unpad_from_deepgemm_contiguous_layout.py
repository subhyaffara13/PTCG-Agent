
def _unpad_from_deepgemm_contiguous_layout(x_padded: torch.Tensor, sorted_to_padded: torch.Tensor) -> torch.Tensor:
    return x_padded[sorted_to_padded]

