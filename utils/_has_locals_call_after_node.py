
def _has_locals_call_after_node(stmt: nodes.NodeNG, scope: nodes.FunctionDef) -> bool:
    skip_nodes = (
        nodes.FunctionDef,
        nodes.ClassDef,
        nodes.Import,
        nodes.ImportFrom,
    )
    for call in scope.nodes_of_class(nodes.Call, skip_klass=skip_nodes):
        inferred = utils.safe_infer(call.func)
        if (
            utils.is_builtin_object(inferred)
            and getattr(inferred, "name", None) == "locals"
        ):
            if stmt.lineno < call.lineno:
                return True
    return False

