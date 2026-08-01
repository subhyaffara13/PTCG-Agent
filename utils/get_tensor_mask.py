
def get_tensor_mask(tensor_list: Iterable[Any]) -> list[bool]:
    return [bool(isinstance(v, torch.Tensor)) for v in tensor_list]

