
def nll_loss2d_backward(
    grad_output: Tensor,
    self: Tensor,
    target: Tensor,
    weight: Tensor | None,
    reduction: int,
    ignore_index: int,
    total_weight: Tensor,
) -> Tensor:
    if self.dim() != 4:
        raise AssertionError(
            f"only batches of spatial inputs supported (4D tensors), but got input of dimension: {self.dim()}"
        )

    if target.dim() != 3:
        raise AssertionError(
            f"only batches of spatial targets supported (3D tensors) but got targets of dimension: {target.dim()}"
        )

    if not (
        self.shape[0] == target.shape[0]
        and self.shape[2] == target.shape[1]
        and self.shape[3] == target.shape[2]
    ):
        raise AssertionError(
            f"size mismatch (got input: {self.shape}, target: {target.shape}"
        )

    if total_weight.numel() != 1:
        raise AssertionError(
            f"expected total_weight to be a single element tensor, "
            f"got: {total_weight.shape} ( {total_weight.numel()}, elements)"
        )

    return _nll_loss_backward(
        grad_output, self, target, weight, reduction, ignore_index, total_weight
    )

