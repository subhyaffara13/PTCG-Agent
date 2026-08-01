
def erfinv(a):
    return prims.erf_inv(a)


def erfinv(ctx, x):
    xre = ctx._re(x)
    if (xre != x) or (xre < -1) or (xre > 1):
        return ctx.bad_domain("erfinv(x) is defined only for -1 <= x <= 1")
    x = xre
    #if ctx.isnan(x): return x
    if not x: return x
    if x == 1: return ctx.inf
    if x == -1: return ctx.ninf
    if abs(x) < 0.9:
        a = 0.53728*x**3 + 0.813198*x
    else:
        # An asymptotic formula
        u = ctx.ln(2/ctx.pi/(abs(x)-1)**2)
        a = ctx.sign(x) * ctx.sqrt(u - ctx.ln(u))/ctx.sqrt(2)
    ctx.prec += 10
    return ctx.findroot(lambda t: ctx.erf(t)-x, a)


def erfinv(x: ArrayLike) -> Array:
  """The inverse of the error function

  JAX implementation of :obj:`scipy.special.erfinv`.

  Returns the inverse of :func:`~jax.scipy.special.erf`.

  Args:
    x: arraylike, real-valued.

  Returns:
    array containing values of the inverse error function.

  Notes:
     The JAX version only supports real-valued inputs.

  See also:
    - :func:`jax.scipy.special.erf`
    - :func:`jax.scipy.special.erfc`
  """
  x, = promote_args_inexact("erfinv", x)
  return lax.erf_inv(x)

