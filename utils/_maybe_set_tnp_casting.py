
def _maybe_set_tnp_casting(xnp: numpy_utils.NpModule) -> None:
  """If TF numpy mode is not set, make sure `tnp.asarray(1.)` is `tf.float32`.

  If user uses TF without numpy mode, it will create casting issues (for
  example: `tf.float64 + tf.float32` will raise an error).
  To limit the errors encountered, we set `tnp.asarray(1.)` to `tf.float32`
  instead of `tf.float64`.

  If numpy mode is already activated, then no need to do anything, as
  `tf.float64 + tf.float32` will support auto-casting, like Jax and Numpy.

  Args:
    xnp: numpy module.
  """
  if not numpy_utils.lazy.has_tf or xnp is not numpy_utils.lazy.tnp:
    return  # Not tnp module

  if not numpy_utils.lazy.is_tnp_enabled:
    # When TF numpy mode is not enabled, `tnp.asarray(1.)` returns tf.float64,
    # creating conflict because TF do fail for operations like:
    # `tf.float64 + tf.float32`
    from tensorflow.python.ops.numpy_ops import np_dtypes  # pylint: disable=g-import-not-at-top,g-direct-tensorflow-import  # pytype: disable=import-error

    if not np_dtypes.is_prefer_float32():
      np_dtypes.set_prefer_float32(True)

    msg = epy.dedent(
        """
        WARNING: Using array types for TF but without numpy mode enabled. It
        is recommended to activate numpy mode as:

        import tensorflow.experimental.numpy as tnp
        tnp.experimental_enable_numpy_behavior(prefer_float32=True)
    """
    )
    # Use print otherwise this isn't displayed on Colab
    # Could have a `epy.logging` module which auto-print on Colab.
    print(msg)

