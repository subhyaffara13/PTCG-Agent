
def sub(pattern, repl, string, count=0, flags=0, pos=None, endpos=None,
  concurrent=None, timeout=None, ignore_unused=False, **kwargs):
    """Return the string obtained by replacing the leftmost (or rightmost with a
    reverse pattern) non-overlapping occurrences of the pattern in string by the
    replacement repl. repl can be either a string or a callable; if a string,
    backslash escapes in it are processed; if a callable, it's passed the match
    object and must return a replacement string to be used."""
    pat = _compile(pattern, flags, ignore_unused, kwargs, True)
    return pat.sub(repl, string, count, pos, endpos, concurrent, timeout)


def sub(
    a: TensorLikeType | NumberType,
    b: TensorLikeType | NumberType,
    *,
    alpha: NumberType = 1,
):
    """
    Reference implementation of torch.sub
    """

    a, b = _maybe_broadcast(a, b)

    if isinstance(a, TensorLike) and isinstance(b, TensorLike):
        torch._check(
            not utils.is_boolean_dtype(a.dtype) and not utils.is_boolean_dtype(b.dtype),
            lambda: (
                "Subtraction, the `-` operator, with two bool tensors is not supported. "
                "Use the `^` or `logical_xor()` operator instead."
            ),
        )

    if alpha != 1:
        dtype = _binary_op_dtype(a, b)
        python_type = utils.dtype_to_type(dtype)
        if not utils.is_weakly_lesser_type(type(alpha), python_type):
            msg = f"alpha argument of type {type(alpha)} cannot be safely cast to type {python_type}!"
            raise ValueError(msg)
        if isinstance(b, torch.Tensor):
            b = prims.mul(b, alpha)
        else:
            # Carefully not to use prims.mul if b is a scalar / symint.
            # prims.mul always returns a tensor,
            # which will mess with type promotion.
            b = b * alpha

    output = prims.sub(a, b)
    return handle_noncontiguous_outputs([a, b], output)


def sub(g: jit_utils.GraphContext, self, other, alpha=None):
    """
    Consumes sub function and returns the corresponding ONNX operator.

    This function is not meant to be called directly by the user.

    Args:
        g (GraphContext): The graph context.
        self (Tensor): The first operand.
        other (Tensor): The second operand.
        alpha (Optional[Tensor]): A scaling factor to apply to the second operand.
            If `alpha` is not provided, it defaults to 1.

    Returns:
        ONNX operator
    """
    if alpha and symbolic_helper._scalar(symbolic_helper._maybe_get_scalar(alpha)) != 1:
        other = g.op("Mul", other, alpha)
    return g.op("Sub", self, other)


def sub(lhs: _ods_ir.Value, rhs: _ods_ir.Value, overflow_flags, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SubOp(lhs=lhs, rhs=rhs, overflowFlags=overflow_flags, results=results, loc=loc, ip=ip).result


def sub(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise subtraction: :math:`x - y`.

  This function lowers directly to the `stablehlo.subtract`_ operation.

  Args:
    x, y: Input arrays. Must have matching numerical dtypes. If neither
      is a scalar, ``x`` and ``y`` must have the same number of dimensions
      and be broadcast compatible.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the difference
    of each pair of broadcasted entries.

  See also:
    - :func:`jax.numpy.subtract`: NumPy-style subtraction supporting
      inputs with mixed dtypes and ranks.

  .. _stablehlo.subtract: https://openxla.org/stablehlo/spec#subtract
  """
  x, y = core.auto_insert_reshard(x, y)
  return sub_p.bind(x, y)

