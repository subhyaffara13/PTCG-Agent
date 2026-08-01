
def _tensor_to_half_val(t: torch.Tensor) -> list[int]:
    return [half_to_int(x) for x in t.flatten().tolist()]

