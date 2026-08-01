
def _clamp_above_eps(x: Tensor) -> Tensor:
    # We assume positive input for this function
    return x.clamp(min=torch.finfo(x.dtype).eps)

