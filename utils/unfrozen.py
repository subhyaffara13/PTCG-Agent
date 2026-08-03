import sys

def unfrozen(self: _T) -> _T:
  """Returns a lazy deep-copy of the dataclass."""
  global _is_tree_registered
  if not _is_tree_registered:
    jax = sys.modules.get('jax', None)
    if jax is not None:
      jax.tree_util.register_pytree_node_class(_MutableProxy)
    _is_tree_registered = True

  impl = _MutableProxyImpl(obj=self, common=_Common(), is_root=True)
  return impl.public_api

