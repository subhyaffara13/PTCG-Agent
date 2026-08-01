
def choose_qparams_symmetric_tensor_meta(
    input: torch.Tensor, quant_min: int, quant_max: int, eps: float, dtype: torch.dtype
) -> tuple[torch.Tensor, torch.Tensor]:
    return torch.empty(1, dtype=torch.double, device=input.device), torch.empty(
        1, dtype=torch.int64, device=input.device
    )

