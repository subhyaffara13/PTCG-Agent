
def lecun_normal(in_axis: int | Sequence[int] = -2,
                 out_axis: int | Sequence[int] = -1,
                 batch_axis: int | Sequence[int] = (),
                 dtype: DTypeLikeInexact | None = None) -> Initializer:
  """Builds a Lecun normal initializer.

  A `Lecun normal initializer`_ is a specialization of
  :func:`jax.nn.initializers.variance_scaling` where ``scale = 1.0``,
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
  >>> initializer = jax.nn.initializers.lecun_normal()
  >>> initializer(jax.random.key(42), (2, 3), jnp.float32)  # doctest: +SKIP
  Array([[ 0.46700746,  0.8414632 ,  0.8518669 ],
         [-0.61677957, -0.67402434,  0.09683388]], dtype=float32)

  .. _Lecun normal initializer: https://arxiv.org/abs/1706.02515
  """
  return variance_scaling(1.0, "fan_in", "truncated_normal", in_axis=in_axis,
                          out_axis=out_axis, batch_axis=batch_axis, dtype=dtype)

