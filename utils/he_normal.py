
def he_normal(in_axis: int | Sequence[int] = -2,
              out_axis: int | Sequence[int] = -1,
              batch_axis: int | Sequence[int] = (),
              dtype: DTypeLikeInexact | None = None) -> Initializer:
  """Builds a He normal initializer (aka Kaiming normal initializer).

  A `He normal initializer`_ is a specialization of
  :func:`jax.nn.initializers.variance_scaling` where ``scale = 2.0``,
  ``mode="fan_in"``, and ``distribution="truncated_normal"``.

  Args:
    in_axis: axis or sequence of axes of the input dimension in the weights
      array.
    out_axis: axis or sequence of axes of the output dimension in the weights
      array.
    batch_axis: axis or sequence of axes in the weight array that should be
      ignored.
    dtype: the dtype of the weights.

  Returns:
    An initializer.

  Examples:

  >>> import jax, jax.numpy as jnp
  >>> initializer = jax.nn.initializers.he_normal()
  >>> initializer(jax.random.key(42), (2, 3), jnp.float32)  # doctest: +SKIP
  Array([[ 0.6604483 ,  1.1900088 ,  1.2047218 ],
         [-0.87225807, -0.95321447,  0.1369438 ]], dtype=float32)

  .. _He normal initializer: https://arxiv.org/abs/1502.01852
  """
  return variance_scaling(2.0, "fan_in", "truncated_normal", in_axis=in_axis,
                          out_axis=out_axis, batch_axis=batch_axis, dtype=dtype)

