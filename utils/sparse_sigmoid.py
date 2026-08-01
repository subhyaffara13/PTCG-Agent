
def sparse_sigmoid(x: ArrayLike) -> Array:
  r"""Sparse sigmoid activation function.

  Computes the function:

  .. math::

    \mathrm{sparse\_sigmoid}(x) = \begin{cases}
      0, & x \leq -1\\
      \frac{1}{2}(x+1), & -1 < x < 1 \\
      1, & 1 \leq x
    \end{cases}

  This is the twin function of the ``sigmoid`` activation ensuring a zero output
  for inputs less than -1, a 1 output for inputs greater than 1, and a linear
  output for inputs between -1 and 1. It is the derivative of ``sparse_plus``.

  For more information, see `Learning with Fenchel-Young Losses (section 6.2)
  <https://arxiv.org/abs/1901.02324>`_.

  Args:
    x : input array

  Returns:
    An array.

  See also:
    :func:`sigmoid`
  """
  return 0.5 * jnp.clip(x + 1.0, 0.0, 2.0)

