from typing import Any

def device_get(x: Any):
  """Transfer ``x`` to host.

  If ``x`` is a pytree, then the individual buffers are copied in parallel.

  Args:
    x: An array, scalar, Array or (nested) standard Python container thereof
      representing the array to be transferred to host.

  Returns:
    An array or (nested) Python container thereof representing the
    value of ``x``.

  Examples:
    Passing a Array:

    >>> import jax
    >>> x = jax.numpy.array([1., 2., 3.])
    >>> jax.device_get(x)
    array([1., 2., 3.], dtype=float32)

    Passing a scalar (has no effect):

    >>> jax.device_get(1)
    1

  See Also:
    - device_put
    - device_put_sharded
    - device_put_replicated
  """
  with config.explicit_device_get_scope():
    for y in tree_leaves(x):
      try:
        y.copy_to_host_async()
      except AttributeError:
        pass
    return tree_map(_device_get, x)

