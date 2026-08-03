from typing import Optional

def nll_loss_forward(
    self: list[int], target: list[int], weight: Optional[list[int]], reduction: int
) -> tuple[list[int], list[int]]:
    # This is taken shamelessly from the meta function in LossNLL.cpp
    self_dim = len(self)
    target_dim = len(target)
    if not (0 < self_dim <= 2):
        raise AssertionError(f"Expected 0 < self_dim <= 2, but got self_dim={self_dim}")
    if target_dim > 1:
        raise AssertionError(f"Expected target_dim <= 1, but got {target_dim}")
    no_batch_dim = self_dim == 1 and target_dim == 0
    if not (no_batch_dim or (self[0] == target[0])):
        raise AssertionError(
            f"Batch size mismatch: self[0]={self[0]}, target[0]={target[0]}"
        )
    n_classes = self[-1]
    scalar_shape: list[int] = []
    if weight is not None and not (len(weight) == 1 and weight[0] == n_classes):
        raise AssertionError(
            f"Expected weight to be None or have shape [n_classes], "
            f"got {weight} with n_classes={n_classes}"
        )
    if reduction == 0 and self_dim == 2:
        reduction_shape = [self[0]]
    else:
        reduction_shape = scalar_shape
    return reduction_shape, scalar_shape


def nll_loss_forward(
    self: Tensor,
    target: Tensor,
    weight: Tensor | None,
    reduction: int,
    ignore_index: int,
) -> tuple[Tensor, Tensor]:
    if not (self.dim() > 0 and self.dim() <= 2):
        raise AssertionError(f"input tensor should be 1D or 2D, got {self.dim()}D")
    if target.dim() > 1:
        raise AssertionError(
            f"0D or 1D target tensor expected, multi-target not supported, got {target.dim()}D"
        )

    no_batch_dim = self.dim() == 1 and target.dim() == 0
    if not no_batch_dim:
        torch._check(
            self.shape[0] == target.shape[0],
            lambda: f"size mismatch (got input: {self.shape}, target: {target.shape})",
        )

    n_classes = self.shape[-1]

    if weight is not None and not (weight.dim() == 1 and weight.numel() == n_classes):
        raise AssertionError(
            f"weight tensor should be defined either for all {n_classes} classes or no classes "
            f"but got weight tensor of shape: {weight.shape}"
        )

    return _nll_loss_forward(self, target, weight, reduction, ignore_index)

