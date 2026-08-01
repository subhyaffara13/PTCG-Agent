
def remove_draw_parameter_from_composite_strategy(node: FunctionDef) -> FunctionDef:
    """Given that the FunctionDef is decorated with @st.composite, remove the
    first argument (`draw`) - it's always supplied by Hypothesis so we don't
    need to emit the no-value-for-parameter lint.
    """
    assert isinstance(node.args.args, list)
    del node.args.args[0]
    del node.args.annotations[0]
    del node.args.type_comment_args[0]
    return node

