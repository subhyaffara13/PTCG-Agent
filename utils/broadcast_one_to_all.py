from typing import Any, Optional

def broadcast_one_to_all(in_tree, is_source: Optional[bool] = None):
  """Broadcast data from a source host to all other hosts."""
  if is_source is None:
    is_source = process_index() == 0
  return multihost_utils.broadcast_one_to_all(in_tree, is_source=is_source)


def broadcast_one_to_all(in_tree, is_source: Optional[bool] = None):
  """Broadcast data from a source host to all other hosts."""
  if is_pathways_backend():
    return in_tree
  if is_source is None:
    is_source = process_index() == 0
  return multihost_utils.broadcast_one_to_all(in_tree, is_source=is_source)


def broadcast_one_to_all(in_tree: Any, is_source: bool | None = None) -> Any:
  """Broadcast data from a source host (host 0 by default) to all other hosts.

  Args:
    in_tree: pytree of arrays - each array *must* have the same shape across the
      hosts.
    is_source: optional bool denoting whether the caller is the source. Only
      'source host' will contribute the data for the broadcast. If None, then
      host 0 is used.

  Returns:
    A pytree matching in_tree where the leaves now all contain the data from the
    first host.
  """
  if jax.process_count() == 1:
    return jax.tree.map(np.asarray, in_tree)

  if is_source is None:
    is_source = jax.process_index() == 0

  devices: np.ndarray = np.array(
      jax.devices()).reshape(jax.process_count(), jax.local_device_count())
  global_mesh = jax.sharding.Mesh(devices, ('processes', 'local_devices'))
  pspec = P('processes')

  def pre_jit(x):
    if is_source:
      inp = x
    else:
      inp = np.zeros_like(x)
    inp = np.expand_dims(inp, axis=0)
    return host_local_array_to_global_array(inp, global_mesh, pspec)

  def post_jit(x):
    return jax.device_get(x.addressable_data(0))

  in_tree = jax.tree.map(pre_jit, in_tree)
  with jax.set_mesh(global_mesh):
    out_tree = jax.jit(_psum, out_shardings=P())(in_tree)

  return jax.tree.map(post_jit, out_tree)

