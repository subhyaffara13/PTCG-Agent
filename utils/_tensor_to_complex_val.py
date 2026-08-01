
def _tensor_to_complex_val(t: torch.Tensor) -> list[float]:
    return torch.view_as_real(t).flatten().tolist()

