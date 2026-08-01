
def unsqueeze(li: list[int], dim: int):
    dim = maybe_wrap_dim(dim, len(li) + 1)
    out = _copy(li)
    out.insert(dim, 1)
    return out


def unsqueeze(x, dim):
    dim = _validate_dim(x, dim, 1)
    new_shape = list(x.get_size())
    new_shape.insert(dim, sympy.S.One)
    return view(x, new_shape)


def unsqueeze(a: TensorLikeType, dim: int) -> TensorLikeType:
    # Note that unsqueeze canonicalizes with rank + 1 because it allows
    # a new innermost dimension to be specified
    ndim = a.ndim + 1
    dim = utils.canonicalize_dim(ndim, dim)
    return prims.expand_dims(a, (dim,), ndim=ndim)


def unsqueeze(g: jit_utils.GraphContext, self, dim):
    if symbolic_helper._is_constant(dim):
        dim = symbolic_helper._get_const(dim, "i", "dim")

    return symbolic_helper._unsqueeze_helper(g, self, [dim])


def unsqueeze(g: jit_utils.GraphContext, self, dim):
    """Implement unsqueezing a pytorch tensor in ONNX by inserting a new dimension at the specified `dim`"""
    # Handle negative dim
    if dim < 0:
        rank = symbolic_helper._get_tensor_rank(self)
        if rank is not None:
            warnings.warn(
                "ONNX export unsqueeze with negative axis "
                + str(dim)
                + " might cause the onnx model to be incorrect. "
                + "Negative axis is not supported in ONNX. "
                + "Axis is converted to "
                + str(dim + rank + 1)
                + " based on input shape at export time. "
                + "Passing an tensor of different rank in execution will be incorrect.",
                stacklevel=2,
            )
            dim = dim + rank + 1
        else:
            return symbolic_helper._unimplemented(
                "unsqueeze", "negative axis with unknown input rank", self
            )

    return symbolic_helper._unsqueeze_helper(g, self, axes_i=[dim])

