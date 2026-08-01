
def restore_args_from_target(target: Any, mesh: Mesh | None = None) -> Any:
  """Creates Orbax `restore_args` given a target Pytree.

  Args:
    target: The Pytree that has the same structure as the checkpoint. The arrays
      restored from checkpoint will have the same `sharding` as the target
      Pytree's corresponding arrays.
    mesh: DEPRECATED ARG. Please simply use your mesh to create the arrays
      in your `target`, no need to pass it here.

  Returns:
    A Pytree of Orbax `RestoreArgs` or `ArrayRestoreArgs`
  """

  def find_sharding(x):
    if hasattr(x, 'sharding'):
      return x.sharding
    return None

  # Simpler case: no JAX arrays
  if not any(
      jax.tree_util.tree_flatten(jax.tree_util.tree_map(find_sharding, target))[
          0
      ]
  ):
    return jax.tree_util.tree_map(
        lambda x: ocp.RestoreArgs(restore_type=np.ndarray), target
    )

  # JAX arrays: find sharding from the given target and create RestoreArgs
  sharding_tree = jax.tree_util.tree_map(find_sharding, target)
  if mesh is not None:
    warnings.warn(
        (
            'restore_args_from_target(): `mesh` arg is deprecated. Simply'
            ' calling the function with target pytree should suffice.'
        ),
        DeprecationWarning,
    )
    def substitute_embedding(s):
      return jax.sharding.NamedSharding(mesh, s.spec)
    sharding_tree = jax.tree_util.tree_map(substitute_embedding, sharding_tree)
  restore_args = ocp.checkpoint_utils.construct_restore_args(
      target, sharding_tree, set_global_shape=False
  )
  return restore_args

