
def round_dec(x: torch.Tensor, decimals: int = 0) -> torch.Tensor:
    ten_pow_decimals = 10.0**decimals
    return aten.round(x * ten_pow_decimals) * (1.0 / ten_pow_decimals)

