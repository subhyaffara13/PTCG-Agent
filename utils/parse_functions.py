
def parse_functions(p):
    with open(p, 'r', encoding='utf-8') as f:
        src = f.read()
    try:
        tree = ast.parse(src, filename=str(p))
    except SyntaxError:
        return []
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

