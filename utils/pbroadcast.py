
def pbroadcast(x, axis_name, source):
  """Perform a collective broadcast and replicate from ``source``.

  This is equivalent to::

    def pbroadcast(x, axis_name, source):
      masked = jnp.where(axis_index(axis_name) == source, x, zeros_like(x))
      return psum(masked, axis_name)

  but implemented in a hardware optimized way.

  If ``x`` is a pytree then the result is equivalent to mapping this function to
  each leaf in the tree.

  This function is an analog of the CollectiveBroadcast HLO.

  Args:
    x: array(s) with a mapped axis named ``axis_name``.
    axis_name: hashable Python object used to name a pmapped axis (see the
      :func:`jax.pmap` documentation for more details).
    source: int, representing which index into ``axis_name`` that should be copied.

  Returns:
    Array(s) with ``x`` being copied from the ``source`` index slice of ``axis_name``.
  """
  return _pbroadcast_is_async(x, axis_name, source, is_async=False)

