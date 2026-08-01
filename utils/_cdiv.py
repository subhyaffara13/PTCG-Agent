
def _cdiv(a: int, b: int) -> int:
    """Ceiling division."""
    return (a + b - 1) // b


def _cdiv(x: int | float | torch.Tensor, multiple: int | float | torch.Tensor):
    return (x + multiple - 1) // multiple

