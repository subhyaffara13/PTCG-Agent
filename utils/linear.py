from typing import Optional

def linear(x, weight, bias):
    return x @ weight.T + bias


def linear(middle: float, pos: float) -> float:
    if pos <= middle:
        if middle < EPSILON:
            return 0.0
        else:
            return 0.5 * pos / middle
    else:
        pos = pos - middle
        middle = 1.0 - middle
        if middle < EPSILON:
            return 1.0
        else:
            return 0.5 + 0.5 * pos / middle


def linear(input: list[int], weight: list[int], bias: Optional[list[int]]):
    out = matmul(input, t(weight))
    if bias is not None:
        if broadcast(bias, out) != out:
            raise AssertionError(
                f"Bias shape {bias} is not broadcastable to output shape {out}"
            )
    return out


def linear(g: jit_utils.GraphContext, input, weight, bias):
    rank = symbolic_helper._get_tensor_rank(input)
    weight = t(g, weight)
    if rank == 2 and not bias.node().mustBeNone():
        alpha = g.op("Constant", value_t=torch.tensor(1, dtype=torch.int64))
        beta = g.op("Constant", value_t=torch.tensor(1, dtype=torch.int64))
        output = addmm(g, bias, input, weight, alpha, beta)
    else:
        output = matmul(g, input, weight)
        if not bias.node().mustBeNone():
            output = add(g, bias, output)

    return output


def linear(
    input: Tensor,
    weight: Tensor,
    bias: Tensor | None = None,
    scale: float | None = None,
    zero_point: int | None = None,
) -> Tensor:
    r"""
    Applies a linear transformation to the incoming quantized data:
    :math:`y = xA^T + b`.
    See :class:`~torch.ao.nn.quantized.Linear`

    .. note::

      Current implementation packs weights on every call, which has penalty on performance.
      If you want to avoid the overhead, use :class:`~torch.ao.nn.quantized.Linear`.

    Args:
      input (Tensor): Quantized input of type `torch.quint8`
      weight (Tensor): Quantized weight of type `torch.qint8`
      bias (Tensor): None or fp32 bias of type `torch.float`
      scale (double): output scale. If None, derived from the input scale
      zero_point (long): output zero point. If None, derived from the input zero_point

    Shape:
        - Input: :math:`(N, *, in\_features)` where `*` means any number of
          additional dimensions
        - Weight: :math:`(out\_features, in\_features)`
        - Bias: :math:`(out\_features)`
        - Output: :math:`(N, *, out\_features)`
    """
    if scale is None:
        scale = input.q_scale()
    if zero_point is None:
        zero_point = input.q_zero_point()
    _packed_params = torch.ops.quantized.linear_prepack(weight, bias)
    return torch.ops.quantized.linear(input, _packed_params, scale, zero_point)


def linear(r, xp):
    return -r

