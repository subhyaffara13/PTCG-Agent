
def glorot_uniform(in_axis: int | Sequence[int] = -2,
                   out_axis: int | Sequence[int] = -1,
                   batch_axis: int | Sequence[int] = (),
                   dtype: DTypeLikeInexact | None = None) -> Initializer:
  """Builds a Glorot uniform initializer (aka Xavier uniform initializer).

  A `Glorot uniform initializer`_ is a specialization of
  :func:`jax.nn.initializers.variance_scaling` where ``scale = 1.0``,
  ``mode="fan_avg"``, and ``distribution="uniform"``.

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
  >>> initializer = jax.nn.initializers.glorot_uniform()
  >>> initializer(jax.random.key(42), (2, 3), jnp.float32)  # doctest: +SKIP
  Array([[ 0.50350785,  0.8088631 ,  0.81566876],
         [-0.6393332 , -0.6865721 ,  0.11003882]], dtype=float32)

  .. _Glorot uniform initializer: http://proceedings.mlr.press/v9/glorot10a.html
  """
  return variance_scaling(1.0, "fan_avg", "uniform", in_axis=in_axis,
                          out_axis=out_axis, batch_axis=batch_axis, dtype=dtype)

