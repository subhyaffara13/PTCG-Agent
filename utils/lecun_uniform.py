
def lecun_uniform(in_axis: int | Sequence[int] = -2,
                  out_axis: int | Sequence[int] = -1,
                  batch_axis: int | Sequence[int] = (),
                  dtype: DTypeLikeInexact | None = None) -> Initializer:
  """Builds a Lecun uniform initializer.

  A `Lecun uniform initializer`_ is a specialization of
  :func:`jax.nn.initializers.variance_scaling` where ``scale = 1.0``,
  ``mode="fan_in"``, and ``distribution="uniform"``.

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
  >>> initializer = jax.nn.initializers.lecun_uniform()
  >>> initializer(jax.random.key(42), (2, 3), jnp.float32)  # doctest: +SKIP
  Array([[ 0.56293887,  0.90433645,  0.9119454 ],
         [-0.71479625, -0.7676109 ,  0.12302713]], dtype=float32)

  .. _Lecun uniform initializer: https://arxiv.org/abs/1706.02515
  """
  return variance_scaling(1.0, "fan_in", "uniform", in_axis=in_axis,
                          out_axis=out_axis, batch_axis=batch_axis, dtype=dtype)

