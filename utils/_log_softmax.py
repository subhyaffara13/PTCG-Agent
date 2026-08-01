
def _log_softmax(x: Tensor, dim: int, half_to_float: bool):
    from torch.fx.experimental.symbolic_shapes import guard_or_false

    # eager log_softmax returns a contiguous tensor. Ensure that decomp also
    # returns a contiguous tensor.
    x = x.contiguous()
    if half_to_float:
        if x.dtype != torch.half:
            raise AssertionError(
                f"half_to_float is True but x.dtype is {x.dtype}, expected torch.half"
            )
    computation_dtype, result_dtype = utils.elementwise_dtypes(
        x, type_promotion_kind=utils.ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )
    x = x.to(computation_dtype)
    if guard_or_false(x.numel() == 0):
        shifted = x
    else:
        x_max = torch.amax(x, dim, keepdim=True)
        shifted = x - x_max
    shifted_logsumexp = torch.log(torch.sum(torch.exp(shifted), dim, keepdim=True))
    result = shifted - shifted_logsumexp
    if not half_to_float:
        result = result.to(result_dtype)
    return result


def _log_softmax(g: jit_utils.GraphContext, input, dim, half_to_float):
    if (
        half_to_float
        and _type_utils.JitScalarType.from_value(
            input, _type_utils.JitScalarType.UNDEFINED
        )
        == _type_utils.JitScalarType.HALF
    ):
        input = g.op("Cast", input, to_i=_C_onnx.TensorProtoDataType.FLOAT)
    return log_softmax(g, input, dim)


def _log_softmax(x, dim, half_to_float, mesh, mesh_dim):
    if half_to_float:
        if x.dtype != torch.half:
            raise AssertionError
    computation_dtype, result_dtype = utils.elementwise_dtypes(
        x, type_promotion_kind=utils.ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )
    x = x.to(dtype=computation_dtype, memory_format=torch.contiguous_format)
    if x.numel() == 0:
        shifted = x
    else:
        x_max = torch.amax(x, dim, keepdim=True)
        x_max = funcol.all_reduce(
            x_max, reduceOp=c10d.ReduceOp.MAX.name, group=(mesh, mesh_dim)
        )
        shifted = x - x_max
    shifted_sumexp = torch.sum(torch.exp(shifted), dim, keepdim=True)
    shifted_sumexp = funcol.all_reduce(
        shifted_sumexp, reduceOp=c10d.ReduceOp.SUM.name, group=(mesh, mesh_dim)
    )
    shifted_logsumexp = torch.log(shifted_sumexp)
    result = shifted - shifted_logsumexp
    if not half_to_float:
        result = result.to(result_dtype)
    return result

