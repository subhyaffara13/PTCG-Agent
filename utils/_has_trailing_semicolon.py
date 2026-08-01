
def _has_trailing_semicolon(
    code_lines: list[str],
    node: ast.AST,
) -> _LineInfo:
  """Check if `node` has trailing `;`."""
  if isinstance(node, ast.AnnAssign) and node.value is None:
    # `AnnAssign().value` can be `None` (`a: int`), do not print anything
    return _LineInfo(
        has_trailing=False,
        options=set(),
        line_num=-1,
    )

  # Extract the lines of the statement
  line_num = node.end_lineno - 1  # pytype: disable=attribute-error
  last_line = code_lines[line_num]  # lineno starts at `1`

  # `node.end_col_offset` is in bytes, so UTF-8 characters count 3.
  last_part_of_line = last_line.encode('utf-8')
  last_part_of_line = last_part_of_line[node.end_col_offset :]  # pytype: disable=attribute-error
  last_part_of_line = last_part_of_line.decode('utf-8')

  # Check if the last character is a `;` token
  has_trailing = False
  options = set()
  if match := _detect_trailing_regex().match(last_part_of_line):
    has_trailing = True
    if match.group('options'):
      options = match.group('options')
      options = {_Options(o) for o in options}

  return _LineInfo(
      has_trailing=has_trailing,
      options=options,
      line_num=line_num,
  )

