
def choose_qparams_tensor_meta(
    input: torch.Tensor, quant_min: int, quant_max: int, eps: float, dtype: torch.dtype
) -> tuple[torch.Tensor, torch.Tensor]:
    if input.dtype not in [
        torch.float32,
        torch.float16,
        torch.bfloat16,
    ]:
        raise AssertionError(
            f"Expecting input to have dtype torch.float32/16/b16, but got dtype: {input.dtype}"
        )
    if quant_min >= quant_max:
        raise AssertionError(
            f"Expecting quant_min to be smaller than quant_max but received min: {quant_min} max: {quant_max}"
        )
    return torch.empty(1, dtype=torch.double, device=input.device), torch.empty(
        1, dtype=torch.int64, device=input.device
    )

