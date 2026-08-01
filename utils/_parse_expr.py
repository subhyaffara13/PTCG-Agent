
def _parse_expr(code: str) -> ast.AST:
  return ast.parse(code, mode='eval').body

