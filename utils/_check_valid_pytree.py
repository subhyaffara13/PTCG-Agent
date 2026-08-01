
def _check_valid_pytree(
  node: tp.Any, fn_name: str, path: str = '',
) -> None:
  from flax.nnx import pytreelib
  if (
    isinstance(node, pytreelib.Pytree)
    and not node._pytree__is_pytree
  ):
    msg = (
      f"Cannot use '{fn_name}' with graph=False on a "
      f"'{type(node).__name__}' instance that has pytree=False. "
    )
    if path:
      msg += f"Found at path: {path}. "
    msg += (
      f"Pytree subclasses with pytree=False are not registered as "
      f"JAX pytrees and cannot be used in tree-mode. "
      + _tree_mode_suggestion_api(fn_name)
    )
    raise ValueError(msg)

