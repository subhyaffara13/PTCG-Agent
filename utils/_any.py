
def _any(input: Tensor, dim: tuple, keepdim: bool):
    # Support torch.any with tuple dim argument.
    # Workaround of https://github.com/pytorch/pytorch/issues/56586
    r = input
    for d in reversed(dim):
        r = r.any(dim=d, keepdim=keepdim)
    return r


def _any(g: jit_utils.GraphContext, *args):
    # aten::any(Tensor self)
    if len(args) == 1:
        input = args[0]
        dim, keepdim = None, 0
    # aten::any(Tensor self, int[]? dim, bool keepdim)
    else:
        input, dim, keepdim = args
        # Can be int list or single int
        dim = symbolic_helper._parse_arg(dim, "t")
        dim = [int(d) for d in dim.view(-1)]
        keepdim = symbolic_helper._parse_arg(keepdim, "i")
    input = g.op("Cast", input, to_i=_C_onnx.TensorProtoDataType.INT64)
    input_sum = symbolic_helper._reducesum_helper(
        g, input, axes_i=dim, keepdims_i=keepdim
    )
    return gt(g, input_sum, g.op("Constant", value_t=torch.tensor(0, dtype=torch.long)))


def _any(x) -> bool:
    return x is not None and com.any_not_none(*x)


def _any(a, axis=None, dtype=None, out=None, keepdims=False, *, where=True):
    # By default, return a boolean for any and all
    if dtype is None:
        dtype = bool_dt
    # Parsing keyword arguments is currently fairly slow, so avoid it for now
    if where is True:
        return umr_any(a, axis, dtype, out, keepdims)
    return umr_any(a, axis, dtype, out, keepdims, where=where)


def _any(predicates: Array) -> Array:
  f = _const(predicates, False)
  predicates_shape = predicates.shape
  all_dimensions = tuple(range(len(predicates_shape)))
  return reduce(predicates, f, bitwise_or, all_dimensions)


def _any(self: Array, axis: reductions.Axis = None, out: None = None,
         keepdims: bool = False, *, where: ArrayLike | None = None) -> Array:
  """Test whether any array elements along a given axis evaluate to True.

  Refer to :func:`jax.numpy.any` for the full documentation.
  """
  return reductions.any(self, axis=axis, out=out, keepdims=keepdims, where=where)

