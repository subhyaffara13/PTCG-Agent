
def _looks_like_typedDict(  # pylint: disable=invalid-name
    node: nodes.FunctionDef | nodes.ClassDef,
) -> bool:
    """Check if node is TypedDict FunctionDef."""
    return node.qname() in TYPING_TYPEDDICT_QUALIFIED

