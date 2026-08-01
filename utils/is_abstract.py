
def is_abstract(tensor: torch.Tensor) -> bool:
    if tensor.is_meta:
        return True
    if torch._subclasses.fake_tensor.is_fake(tensor):
        return True
    return False

