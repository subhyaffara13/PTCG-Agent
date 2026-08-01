
def logit(self: TensorLikeType, eps: float | None = None) -> TensorLikeType:
    if eps is None:
        eps = -1.0
    lo = eps
    hi = 1 - eps
    self = torch.where(self < lo, lo, torch.where(self > hi, hi, self))
    return torch.log(torch.true_divide(self, torch.sub(1, self)))


def logit(g: jit_utils.GraphContext, self: torch._C.Value, eps: torch._C.Value):
    one = g.op("Constant", value_t=torch.tensor(1.0))

    if not symbolic_helper._is_none(eps):
        eps = g.op(
            "Cast", eps, to_i=_type_utils.JitScalarType.from_value(self).onnx_type()
        )
        one_sub_eps = g.op("Sub", one, eps)
        self_less_equal_one_sub_eps = g.op("Greater", one_sub_eps, self)
        temporary_self = g.op("Where", self_less_equal_one_sub_eps, self, one_sub_eps)

        temporary_self_less_eps = g.op("Less", temporary_self, eps)
        z = g.op("Where", temporary_self_less_eps, eps, temporary_self)
    else:
        z = self

    sub = g.op("Sub", one, z)
    div = g.op("Div", z, sub)
    return g.op("Log", div)


def logit(x: ArrayLike) -> Array:
  r"""The logit function

  JAX implementation of :obj:`scipy.special.logit`.

  .. math::

     \mathrm{logit}(p) = \log\frac{p}{1 - p}

  Args:
    x: arraylike, real-valued.

  Returns:
    array containing values of the logit function.
  """
  x, = promote_args_inexact("logit", x)
  return lax.log(lax.div(x, lax.sub(_lax_const(x, 1), x)))

