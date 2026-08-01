
def build_mismatched_tree_structure_error(
    source_tree: PyTreeOf[Any],
    target_tree: PyTreeOf[Any],
    log_message: str,
    exception_cls: Type[_ErrorType] = TreeStructureError,
) -> Type[_ErrorType]:
  """Builds a TreeStructureError pointing to where exactly two trees differ."""
  if isinstance(source_tree, parts_of.PartsOf):
    source_tree = source_tree.unsafe_structure
  if isinstance(target_tree, parts_of.PartsOf):
    target_tree = target_tree.unsafe_structure

  diff = tree_difference(
      source_tree,
      target_tree,
      leaves_equal=operator.eq,
  )

  if diff is None:
    return exception_cls(f'{log_message}. But no diff was found.')

  formatted_diff = format_tree_diff(diff)
  return exception_cls(f'{log_message}.\n\n{formatted_diff}')

