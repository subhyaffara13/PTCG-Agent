
def view_copy_default(
    self: torch.Tensor,
    size: list[int | torch.SymInt],
) -> torch.Tensor:
    return aten.view(self, size).clone()

