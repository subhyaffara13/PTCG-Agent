
def ndtr(a: TensorLikeType) -> TensorLikeType:
    # Note: M_SQRT1_2 is the value of 1 / sqrt(2)
    M_SQRT1_2 = 0.707106781186547524400844362104849039
    a_sqrt_2 = a * M_SQRT1_2
    return (1 + torch.erf(a_sqrt_2)) * 0.5


def ndtr(x: ArrayLike) -> Array:
  r"""Normal distribution function.

  JAX implementation of :obj:`scipy.special.ndtr`.

  Returns the area under the Gaussian probability density function, integrated
  from minus infinity to x:

  .. math::
    \begin{align}
    \mathrm{ndtr}(x) =&
      \ \frac{1}{\sqrt{2 \pi}}\int_{-\infty}^{x} e^{-\frac{1}{2}t^2} dt \\
    =&\ \frac{1}{2} (1 + \mathrm{erf}(\frac{x}{\sqrt{2}})) \\
    =&\ \frac{1}{2} \mathrm{erfc}(\frac{x}{\sqrt{2}})
    \end{align}

  Args:
    x: An array of type `float32`, `float64`.

  Returns:
    An array with `dtype=x.dtype`.

  Raises:
    TypeError: if `x` is not floating-type.
  """
  x = jnp.asarray(x)
  dtype = lax.dtype(x)
  if dtype not in (np.float32, np.float64):
    raise TypeError(
        "x.dtype={} is not supported, see docstring for supported types."
        .format(dtype))
  return _ndtr(x)

