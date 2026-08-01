
def _extract_nested_case(
    case_node: c_ast.Case | c_ast.Default, stmts_list: List[c_ast.Node]
) -> None:
    """Recursively extract consecutive Case statements that are made nested
    by the parser and add them to the stmts_list.
    """
    if isinstance(case_node.stmts[0], (c_ast.Case, c_ast.Default)):
        nested = case_node.stmts.pop()
        stmts_list.append(nested)
        _extract_nested_case(cast(Any, nested), stmts_list)

