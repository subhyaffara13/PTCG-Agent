
def _copy_to_aten(a: Tensor, b: Tensor) -> Tensor:
    return a.copy_(b)

