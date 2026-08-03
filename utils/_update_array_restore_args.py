from typing import Any

def _update_array_restore_args(
    v: Any, leaf_args: ArrayRestoreArgs
) -> ArrayRestoreArgs:
  """Updates ArrayRestoreArgs with global shape and dtype."""
  if isinstance(v, type):
    return leaf_args
  is_array = getattr(v, 'shape', False) and getattr(v, 'dtype', False)
  is_prng_key = jax.dtypes.issubdtype(
      getattr(v, 'dtype', None), jax.dtypes.prng_key
  )
  if is_array and not is_prng_key:
    updates = {}
    if leaf_args.strict:
      if leaf_args.global_shape is None and leaf_args.shape is None:
        updates['global_shape'] = getattr(v, 'shape', None)
      if getattr(leaf_args, 'dtype', None) is None:
        updates['dtype'] = getattr(v, 'dtype', None)
    if updates:
      return dataclasses.replace(leaf_args, **updates)
  return leaf_args

