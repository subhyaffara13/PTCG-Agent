
def glorot_normal(in_axis: int | Sequence[int] = -2,
                  out_axis: int | Sequence[int] = -1,
                  batch_axis: int | Sequence[int] = (),
                  dtype: DTypeLikeInexact | None = None) -> Initializer:
  """Builds a Glorot normal initializer (aka Xavier normal initializer).

  A `Glorot normal initializer`_ is a specialization of
  :func:`jax.nn.initializers.variance_scaling` where ``scale = 1.0``,
  ``mode="fan_avg"``, and ``distribution="truncated_normal"``.

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
  >>> initializer = jax.nn.initializers.glorot_normal()
  >>> initializer(jax.random.key(42), (2, 3), jnp.float32)  # doctest: +SKIP
  Array([[ 0.41770416,  0.75262755,  0.7619329 ],
         [-0.5516644 , -0.6028657 ,  0.08661086]], dtype=float32)

  .. _Glorot normal initializer: http://proceedings.mlr.press/v9/glorot10a.html
  """
  return variance_scaling(1.0, "fan_avg", "truncated_normal", in_axis=in_axis,
                          out_axis=out_axis, batch_axis=batch_axis, dtype=dtype)

