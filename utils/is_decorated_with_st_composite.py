
def is_decorated_with_st_composite(node: FunctionDef) -> bool:
    """Return whether a decorated node has @st.composite applied."""
    if node.decorators and node.args.args and node.args.args[0].name == "draw":
        for decorator_attribute in node.decorators.nodes:
            if decorator_attribute.as_string() in COMPOSITE_NAMES:
                return True
    return False

