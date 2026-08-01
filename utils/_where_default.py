
def _where_default(pred: Tensor) -> tuple[Tensor, ...]:
    return torch.nonzero(pred, as_tuple=True)

