
def _tensor_to_list(t: torch.Tensor) -> list[Any]:
    return t.flatten().tolist()

