
def _is_name_main_check(node):
    """Check if an ast.If tests __name__ == '__main__'."""
    if not isinstance(node, ast.If):
        return False
    return (isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name) and node.test.left.id == '__name__'
            and len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.Eq)
            and len(node.test.comparators) == 1
            and isinstance(node.test.comparators[0], ast.Constant)
            and node.test.comparators[0].value == '__main__')

