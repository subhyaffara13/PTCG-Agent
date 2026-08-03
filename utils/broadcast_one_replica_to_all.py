import functools
import logging
from typing import Optional, Union

def broadcast_one_replica_to_all(
    in_tree: tuple[jax.Array, ...],
    global_mesh: jax.sharding.Mesh,
    replica_axis_index: int,
    is_source: bool,
    memory_limit_bytes: Optional[Union[int, None]] = None,
    memory_scaling_factor: Optional[float] = 0.75,
) -> tuple[tuple[jax.Array, ...], int]:
  """One replica reads the data and broadcasts to others.

  Args:
    in_tree: pytree to be broadcast. Shardings should correspond to the origin
      replica.
    global_mesh: global mesh.
    replica_axis_index: axis index along which the data is replicated.
    is_source: indicates if the current host is in origin replica.
    memory_limit_bytes: memory limit for broadcasting in bytes.
    memory_scaling_factor: indicates the fraction of the estimated available
      memory to be used when broadcasting data.

  Returns:
     Tuple containing:
      - pytree with broadcasted data
      - number of broadcasts performed.
  """
  if memory_limit_bytes is None:
    memory_limit_bytes = get_available_memory(in_tree, memory_scaling_factor)
    logging.info('Using available memory of %d bytes.', memory_limit_bytes)

  tree_len = len(in_tree)
  start = 0
  out_tree = []
  num_broadcasts = 0
  while start < tree_len:
    subtree = []
    current_memory = 0
    end = start
    if tree_memory_per_device(in_tree[start]) > memory_limit_bytes:
      logging.warning(
          'in_tree leaf size exceeds memory limit for broadcasting. '
          'Leaf size: %d bytes. Allowed memory limit: %d bytes. Proceeding.',
          tree_memory_per_device(in_tree[start]),
          memory_limit_bytes,
      )
      subtree.append(in_tree[end])
      end += 1
    else:
      while end < tree_len and (
          current_memory + tree_memory_per_device(in_tree[end])
          <= memory_limit_bytes
      ):
        subtree.append(in_tree[end])
        current_memory += tree_memory_per_device(in_tree[end])
        end += 1
    subtree = tuple(subtree)
    num_broadcasts += 1
    globalized_sharded_subtree = jax.tree.map(
        functools.partial(
            _globalize_single_replica_arrays,
            global_mesh=global_mesh,
            replica_axis_index=replica_axis_index,
            is_source=is_source,
        ),
        subtree,
    )
    # Delete immediately to conserve memory.
    jax.tree.map(lambda x: x.delete(), subtree)
    out_subtree = _merge_globalized_replicas(
        globalized_sharded_subtree, global_mesh
    )
    out_tree.extend(out_subtree)
    jax.block_until_ready(out_subtree)
    start = end

  if is_source:
    logging.info('Total number of broadcasts: %d', num_broadcasts)
  return tuple(out_tree), num_broadcasts

