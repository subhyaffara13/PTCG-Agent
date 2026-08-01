
def _div_if_needed(tensor: torch.Tensor, div_factor: float) -> None:
    if div_factor > 1:
        tensor.div_(div_factor)


def _div_if_needed(tensor: torch.Tensor, div_factor: float | None) -> None:
    if div_factor is not None and div_factor != 1:
        tensor.div_(div_factor)

