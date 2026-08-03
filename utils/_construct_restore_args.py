import functools
from typing import Any, Callable

def _construct_restore_args(
    target: PyTree | None,
    metadata: Callable[[], tree_metadata.TreeMetadata],
    fallback_sharding: jax.sharding.Sharding | None,
    support_layout: bool = False,
) -> PyTree:
  """Creates restore_args given a target tree and sharding tree we construct.

  If target tree does not exist, use metadata_tree as target tree.

  Overrides the sharding in `target tree` with fallback_sharding if the sharding
  in `target tree` is either missing or incompatible with the current device
  mesh.

  Accounts for the following cases:
    - sharding exists and is in target tree leaf (use target sharding)
    - sharding missing in target but exists in metadata tree leaf (fallback to
      metadata sharding)
    - sharding in metadata tree leaf is incompatible with current device mesh
      (fallback to fallback_sharding)

  Args:
    target: The returned TreeMetadata will match the structure of `target`.
    metadata: A callable that returns the metadata to be used as target if
      target is none or as fallback sharding.
    fallback_sharding: If provided, this sharding is used as fallback if the
      sharding in `target` fails to load from the checkpoint.
    support_layout: If true, layout is extracted instead of explicit sharding.

  Returns:
    A PyTree matching target of RestoreArgs (or ArrayRestoreArgs) objects.
  """

  @functools.lru_cache(maxsize=1)
  def _get_loaded_metadata():
    return metadata()

  @functools.lru_cache(maxsize=1)
  def _get_flat_metadata():
    return tree_utils.to_flat_dict(_get_loaded_metadata().tree)

  def _get_sharding_from_metadata_leaf(metadata_leaf):
    if (
        isinstance(metadata_leaf, value_metadata.ArrayMetadata)
        and metadata_leaf.sharding is not None
    ):
      try:
        return metadata_leaf.sharding.to_jax_sharding()
      except ValueError as e:
        if fallback_sharding is not None:
          return fallback_sharding
        raise ValueError(
            'Topology mismatch detected. The checkpoint was saved with'
            ' a different topology than the current one. Please provide'
            ' a target tree with the desired topology to restore.'
        ) from e
    return None

  def _get_sharding_for_target_leaf(
      path: tuple[Any, ...], item_leaf: Any
  ) -> jax.sharding.Sharding | None:
    """Determines the sharding for a given leaf in the target tree."""
    if not hasattr(item_leaf, 'sharding'):
      return None

    # 1. Check sharding on item_leaf itself and return proper sharding format
    sharding = arrays_sharding_lib.get_sharding_or_format(
        item_leaf, support_format=support_layout
    )
    if sharding is not None:
      return sharding

    # 2. If item_leaf.sharding is None, try to get from metadata_tree.
    # We iterate on the target tree and use path-based lookups for metadata
    # because direct jax.tree.map(target, metadata) fails when target contains
    # unregistered custom PyTree nodes (like Flax dataclasses) that don't
    # structurally match the dict-based metadata tree.
    target_path_tuple = tree_utils.tuple_path_from_keypath(path)
    metadata_leaf = _get_flat_metadata().get(target_path_tuple)
    if metadata_leaf is None:
      raise ValueError(
          f'Structure mismatch: Target path {target_path_tuple} not found in'
          ' metadata_tree. Expected identical structures. Metadata keys:'
          f' {_get_flat_metadata().keys()}'
      )

    sharding = _get_sharding_from_metadata_leaf(metadata_leaf)

    return sharding

  if target is not None:
    target_tree = target
    sharding_tree = jax.tree_util.tree_map_with_path(
        _get_sharding_for_target_leaf,
        target_tree,
    )
  else:
    loaded_metadata_tree = _get_loaded_metadata()
    target_tree = loaded_metadata_tree.tree
    sharding_tree = jax.tree_util.tree_map(
        _get_sharding_from_metadata_leaf, loaded_metadata_tree.tree
    )

  return checkpoint_utils.construct_restore_args(target_tree, sharding_tree)

