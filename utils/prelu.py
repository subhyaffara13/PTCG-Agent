
def prelu(a: TensorLikeType, weight: TensorLikeType) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.prelu
    """
    torch._check(
        isinstance(a, TensorLike),
        lambda: f"prelu: Expected `a` to be tensor, but got: {type(a)}",
    )
    torch._check(
        isinstance(weight, TensorLike),
        lambda: f"prelu: Expected `weight` to be tensor, but got: {type(weight)}",
    )

    if weight.numel() != 1:
        torch._check(a.ndim > 0, lambda: "Not allow zero-dim input tensor.")
        channel_size = a.shape[1] if a.ndim >= 2 else 1
        torch._check(
            weight.numel() == channel_size,
            lambda: f"Mismatch of parameter numbers and input channel size. Found parameter numbers ="
            f" {weight.numel()} and channel size = {channel_size}.",
        )

    torch._check(
        weight.ndim == 0 or weight.ndim == 1,
        lambda: f"prelu: Expected `weight` to be a scalar or 1D tensor, but got: "
        f"ndim = {weight.ndim}",
    )
    if a.ndim == 0:
        weight = weight[0] if weight.ndim == 1 else weight
    else:
        weight = prims.broadcast_in_dim(
            weight, a.shape, () if weight.ndim == 0 else (0 if a.ndim == 1 else 1,)
        )

    return torch.where(a > 0, a, a * weight)


def prelu(g: jit_utils.GraphContext, self, weight):
    self_rank = symbolic_helper._get_tensor_rank(self)
    weight_sizes = symbolic_helper._get_tensor_sizes(weight)
    if self_rank is not None and self_rank > 2:
        weight = g.op("Unsqueeze", weight, axes_i=list(range(1, self_rank - 1)))
    elif self_rank == 0 and weight_sizes == [1]:
        # self and weight are both scalar but weight has rank == 1, squeeze weight.
        weight = symbolic_helper._squeeze_helper(g, weight, [0])
    if symbolic_helper._try_get_scalar_type(self):
        old_type, self, weight = _try_cast_integer_to_float(g, self, weight)
        return _cast_to_type(g, g.op("PRelu", self, weight), old_type)
    else:
        return g.op("PRelu", self, weight)


def prelu(g: jit_utils.GraphContext, self, weight):
    self_rank = symbolic_helper._get_tensor_rank(self)
    weight_sizes = symbolic_helper._get_tensor_sizes(weight)
    weight_rank = len(weight_sizes)
    if self_rank is not None:
        if self_rank > 2:
            # make weight unidirectional broadcastable
            weight = symbolic_helper._unsqueeze_helper(
                g, weight, list(range(1, self_rank - 1))
            )
        elif self_rank == 0 and weight_sizes == [1]:
            # self and weight are both scalar but weight has rank == 1, squeeze weight.
            weight = symbolic_helper._squeeze_helper(g, weight, [0])
            weight_rank = 0

    if self_rank is not None and weight_rank is not None:
        if self_rank < weight_rank:
            raise AssertionError(
                f"rank(x) should be >= rank(slope) but got {self_rank} < {weight_rank}"
            )
    return g.op("PRelu", self, weight)

