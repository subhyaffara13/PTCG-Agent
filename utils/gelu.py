
def gelu(x):
    """
    This is the gelu implementation from the original ESM repo. Using F.gelu yields subtly wrong results.
    """
    return x * 0.5 * (1.0 + torch.erf(x / math.sqrt(2.0)))


def gelu(x):
    """
    This is the gelu implementation from the original EVOLLA_SA_PROT repo. Using F.gelu yields subtly wrong results.
    """
    return x * 0.5 * (1.0 + torch.erf(x / math.sqrt(2.0)))


def gelu(a: TensorLikeType, approximate: str = "none") -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.gelu
    """
    if not isinstance(a, TensorLike):
        raise RuntimeError(
            "Expected a tensor input for an elementwise unary operation!"
        )
    M_SQRT2 = 1.41421356237309504880
    M_SQRT1_2 = 0.70710678118654752440
    M_2_SQRTPI = 1.12837916709551257390
    if approximate == "tanh":
        kBeta = M_SQRT2 * M_2_SQRTPI * 0.5
        kKappa = 0.044715
        a_cube = a * a * a
        inner = kBeta * (a + kKappa * a_cube)
        return 0.5 * a * (1 + torch.tanh(inner))
    elif approximate == "none":
        kAlpha = M_SQRT1_2
        return a * 0.5 * (1 + torch.erf(a * kAlpha))
    else:
        raise RuntimeError("approximate argument must be either none or tanh.")


def gelu(g: jit_utils.GraphContext, self: _C.Value, approximate: str = "none"):
    return g.op("Gelu", self, approximate_s=approximate)


def gelu(g: jit_utils.GraphContext, self: torch._C.Value, approximate: str = "none"):
    if approximate == "tanh":
        kBeta = math.sqrt(2 / math.pi)
        kKappa = 0.044715

        beta = torch.tensor(kBeta, dtype=torch.double)
        kappa = torch.tensor(kKappa, dtype=torch.double)
        one = torch.tensor(1.0, dtype=torch.double)
        half = torch.tensor(0.5, dtype=torch.double)

        self_cube = mul(g, self, mul(g, self, self))
        inner = mul(g, beta, add(g, self, mul(g, kappa, self_cube)))
        return mul(g, half, mul(g, self, add(g, one, g.op("Tanh", inner))))
    else:
        _sqrt2 = 1.4142135623730951
        erf = g.op("Erf", g.op("Div", self, torch.tensor(_sqrt2, dtype=torch.double)))
        erf_plusone = add(
            g, erf, g.op("Constant", value_t=torch.tensor(1, dtype=torch.double))
        )
        return mul(
            g,
            mul(g, self, erf_plusone),
            g.op("Constant", value_t=torch.tensor(0.5, dtype=torch.double)),
        )


def gelu(x: ArrayLike, approximate: bool = True) -> Array:
  r"""Gaussian error linear unit activation function.

  If ``approximate=False``, computes the element-wise function:

  .. math::
    \mathrm{gelu}(x) = \frac{x}{2} \left(\mathrm{erfc} \left(
      \frac{-x}{\sqrt{2}} \right) \right)

  If ``approximate=True``, uses the approximate formulation of GELU:

  .. math::
    \mathrm{gelu}(x) = \frac{x}{2} \left(1 + \mathrm{tanh} \left(
      \sqrt{\frac{2}{\pi}} \left(x + 0.044715 x^3 \right) \right) \right)

  For more information, see `Gaussian Error Linear Units (GELUs)
  <https://arxiv.org/abs/1606.08415>`_, section 2.

  Args:
    x: input array
    approximate: whether to use the approximate or exact formulation.
  """
  [x_arr] = numpy_util.promote_args_inexact("gelu", x)

  if approximate:
    sqrt_2_over_pi = np.sqrt(2 / np.pi).astype(x_arr.dtype)
    cdf = 0.5 * (1.0 + jnp.tanh(sqrt_2_over_pi * (x_arr + 0.044715 * (x_arr ** 3))))
    return x_arr * cdf
  else:
    sqrt_half = np.sqrt(0.5).astype(x_arr.dtype)
    return jnp.array(
        0.5 * x_arr * (lax.erfc(-x_arr * sqrt_half)), dtype=x_arr.dtype
    )

