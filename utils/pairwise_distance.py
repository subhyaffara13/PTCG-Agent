
def pairwise_distance(
    x1: TensorLikeType,
    x2: TensorLikeType,
    p: NumberType = 2.0,
    eps: NumberType = 1e-6,
    keepdim=False,
) -> TensorLikeType:
    return torch.linalg.vector_norm(x1 - x2 + eps, ord=p, dim=-1, keepdim=keepdim)


def pairwise_distance(g: jit_utils.GraphContext, input1, input2, p, eps, keepdim):
    if not symbolic_helper._is_value(eps):
        eps = g.op("Constant", value_t=torch.tensor([eps]))
    inv_p = div(
        g,
        g.op("Constant", value_t=torch.tensor([1], dtype=torch.float)),
        add(g, p, eps),
    )
    summation = symbolic_helper._reducesum_helper(
        g,
        # pyrefly: ignore [no-matching-overload]
        pow(g, sub(g, input1, input2), p),
        axes_i=[-1],
        keepdims_i=symbolic_helper._parse_arg(keepdim, "i"),
    )
    # pyrefly: ignore [no-matching-overload]
    return pow(g, summation, inv_p)

