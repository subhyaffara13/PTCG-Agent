
def format_tree_diff(
    diff: PyTree,
    path_prefix: str = '',
    source_label: str = 'Source',
    target_label: str = 'Target',
) -> str | None:
  """Format a tree difference structure into a readable multi-line string.

  Args:
    diff: object representing the difference between two PyTrees
    path_prefix: Current path prefix for nested structures
    source_label: Label for the source value
    target_label: Label for the target value

  Returns:
    A formatted string showing the differences in a multi-line structure.
  """
  source_label = f'    - {source_label}:'
  target_label = f'    - {target_label}:'
  missing_symbol = 'MISSING'

  lines = []

  # Leaf nodes
  if isinstance(diff, Diff):
    if path_prefix:
      lines.append(f'{path_prefix}:')
    else:
      lines.append('Mismatch:')

    def _format_value(value):
      return missing_symbol if value in (None, parts_of.PLACEHOLDER) else value

    lines.append(f'{source_label} {_format_value(diff.lhs)}')
    lines.append(f'{target_label} {_format_value(diff.rhs)}')
    return '\n'.join(lines)

  # Nested nodes
  children, _ = utils.tree_flatten_with_path_one_level(diff)
  for path, value in children:
    key = path[0]
    if value is not None:
      if isinstance(key, jax.tree_util.SequenceKey):
        new_path = f'{path_prefix}[{key.idx}]'
      elif isinstance(key, jax.tree_util.DictKey):
        new_path = f'{path_prefix}.{key.key}' if path_prefix else str(key.key)
      elif isinstance(key, jax.tree_util.GetAttrKey):
        new_path = f'{path_prefix}.{key.name}' if path_prefix else str(key.name)
      else:
        raise ValueError(f'Unsupported key type: {type(key)}')

      formatted = format_tree_diff(value, new_path)
      if formatted:
        lines.append(formatted)
  return '\n\n'.join(lines)

