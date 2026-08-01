
def _is_restore_spec_leaf(value: Any) -> bool:
  """Returns whether the value is a valid restore spec leaf."""
  return isinstance(
      value,
      (
          jax.Array,
          jax.ShapeDtypeStruct,
          type_handlers.ArrayRestoreArgs,
      ),
  )

