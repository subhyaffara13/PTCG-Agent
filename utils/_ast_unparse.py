
def _ast_unparse(node: ast.AST) -> str:
    return ast.unparse(node).replace("\n", "")

