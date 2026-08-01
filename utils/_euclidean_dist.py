
def _euclidean_dist(x1: Tensor, x2: Tensor) -> Tensor:
    x1_norm = x1.pow(2).sum(-1, True)
    x1_pad = torch.ones_like(x1_norm, memory_format=torch.contiguous_format)
    x2_norm = x2.pow(2).sum(-1, True)
    x2_pad = torch.ones_like(x2_norm, memory_format=torch.contiguous_format)
    x1_ = torch.cat([x1.mul(-2), x1_norm, x1_pad], -1)
    x2_ = torch.cat([x2, x2_pad, x2_norm], -1)
    result = x1_.matmul(x2_.mT)
    return result.clamp_min(0).sqrt()


def _euclidean_dist(g: jit_utils.GraphContext, x1, x2):
    # X1.shape = (B * P * D), X2.shape = (B * R * D)
    # using matrix multiplication to accelerate the calculation of
    # the euclidean distance
    rank = symbolic_helper._get_tensor_rank(x1)
    if rank is None:
        raise AssertionError("rank must be non-None")
    x1_norm = symbolic_helper._reducesum_helper(
        g,
        # pyrefly: ignore [no-matching-overload]
        pow(g, x1, symbolic_helper._generate_wrapped_number(g, 2.0)),
        axes_i=[-1],
        keepdims_i=True,
    )
    x1_pad = ones_like(g, x1_norm)
    x2_norm = symbolic_helper._reducesum_helper(
        g,
        # pyrefly: ignore [no-matching-overload]
        pow(g, x2, symbolic_helper._generate_wrapped_number(g, 2.0)),
        axes_i=[-1],
        keepdims_i=True,
    )
    x2_pad = ones_like(g, x2_norm)
    x1_ = g.op(
        "Concat",
        *[
            mul(g, symbolic_helper._generate_wrapped_number(g, -2.0), x1),
            x1_norm,
            x1_pad,
        ],
        axis_i=-1,
    )
    x2_ = g.op("Concat", *[x2, x2_pad, x2_norm], axis_i=-1)
    result = matmul(g, x1_, transpose(g, x2_, -2, -1))
    dtype = _type_utils.JitScalarType.from_value(result)
    min = g.op(
        "Cast", symbolic_helper._generate_wrapped_number(g, 0.0), to_i=dtype.onnx_type()
    )
    result = symbolic_helper._op_with_optional_float_cast(
        g, "Max", result, min, opset_before=12
    )
    result = sqrt(g, result)
    return result


def _euclidean_dist(x):
    return cdist(x, x)

