
def unwrap_maybe_dynamic_int(x: torch.Tensor | int) -> int:
    if isinstance(x, torch.Tensor):
        # x.size() is expected to be [0, dynamic_int]
        return x.size(1)
    return x

