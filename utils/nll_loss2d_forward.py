
def nll_loss2d_forward(
    self: Tensor,
    target: Tensor,
    weight: Tensor | None,
    reduction: int,
    ignore_index: int,
) -> tuple[Tensor, Tensor]:
    return _nll_loss_forward(self, target, weight, reduction, ignore_index)

