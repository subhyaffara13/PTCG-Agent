
def _eval_cycler_expr(node):
    """Recursively evaluate an AST node to build a Cycler object."""
    if isinstance(node, ast.BinOp):
        left = _eval_cycler_expr(node.left)
        right = _eval_cycler_expr(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Mult):
            return left * right
        raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
    if isinstance(node, ast.Call):
        if not (isinstance(node.func, ast.Name)
                and node.func.id in ('cycler', 'concat')):
            raise ValueError(
                "only the 'cycler()' and 'concat()' functions are allowed")
        func = cycler if node.func.id == 'cycler' else cconcat
        args = [_eval_cycler_expr(a) for a in node.args]
        kwargs = {kw.arg: _eval_cycler_expr(kw.value) for kw in node.keywords}
        return func(*args, **kwargs)
    if isinstance(node, ast.Subscript):
        sl = node.slice
        if not isinstance(sl, ast.Slice):
            raise ValueError("only slicing is supported, not indexing")
        s = slice(
            ast.literal_eval(sl.lower) if sl.lower else None,
            ast.literal_eval(sl.upper) if sl.upper else None,
            ast.literal_eval(sl.step) if sl.step else None,
        )
        value = _eval_cycler_expr(node.value)
        return value[s]
    # Allow literal values (int, strings, lists, tuples) as arguments
    # to cycler() and concat().
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError):
        raise ValueError(
            f"Unsupported expression in cycler string: {ast.dump(node)}")

