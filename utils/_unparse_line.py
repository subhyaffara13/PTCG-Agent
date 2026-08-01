
def _unparse_line(node: ast.AST) -> ast.Constant:
  """Extract the line code."""
  if isinstance(node, ast.Assign):
    node = node.targets
  elif isinstance(node, ast.AnnAssign):
    node = node.target
  return ast.Constant(ast.unparse(node))

