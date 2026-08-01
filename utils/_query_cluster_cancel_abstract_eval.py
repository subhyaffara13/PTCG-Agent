
def _query_cluster_cancel_abstract_eval(try_cancel_buffer,
                                        *transforms_leaves,
                                        grid_names,
                                        transforms_tree):
  del try_cancel_buffer, transforms_leaves, transforms_tree
  grid_idxs = (jax_core.ShapedArray((), jnp.int32),) * len(grid_names)
  return (
      (
          *grid_idxs,
          jax_core.ShapedArray((), jnp.bool_),
      ),
      {gpu_core._memory_effect},
  )

