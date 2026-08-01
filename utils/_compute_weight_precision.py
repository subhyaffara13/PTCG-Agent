
def _compute_weight_precision(weights: TensorSequenceType) -> Tensor:
    max_weight = torch.stack(weights).max()
    max_weight_precision = 22
    precisions = torch.arange(max_weight_precision, device=max_weight.device)
    values = 0.5 + max_weight * (1 << (precisions + 1))
    mask = values >= (1 << 15)
    return max_weight_precision - mask.sum()

