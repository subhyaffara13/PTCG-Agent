
def _to_ground_truth(result: Any) -> torch.Tensor | list[torch.Tensor]:
    """Convert an op result to the ground truth format (tensor or list of tensors)."""
    if isinstance(result, torch.Tensor):
        return result
    return list(result)

