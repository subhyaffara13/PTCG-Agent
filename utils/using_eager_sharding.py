
def using_eager_sharding() -> bool:
  """Returns whether Variables are using eager sharding by default.

  Example::

    >>> from flax import nnx
    >>> nnx.use_eager_sharding(True)
    <...>
    >>> nnx.using_eager_sharding()
    True
    >>> nnx.use_eager_sharding(False)
    <...>
    >>> nnx.using_eager_sharding()
    False


  Returns:
    A boolean indicating if Variables are using eager sharding by default.
  """
  return use_eager_sharding.current_value()

