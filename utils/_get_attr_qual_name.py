
def _get_attr_qual_name(node, aliases):
    """Get a the full name for the attribute node.

    This will resolve a pseudo-qualified name for the attribute
    rooted at node as long as all the deeper nodes are Names or
    Attributes. This will give you how the code referenced the name but
    will not tell you what the name actually refers to. If we
    encounter a node without a static name we punt with an
    empty string. If this encounters something more complex, such as
    foo.mylist[0](a,b) we just return empty string.

    :param node: AST Name or Attribute node
    :param aliases: Import aliases dictionary
    :returns: Qualified name referred to by the attribute or name.
    """
    if isinstance(node, ast.Name):
        if node.id in aliases:
            return aliases[node.id]
        return node.id
    elif isinstance(node, ast.Attribute):
        name = f"{_get_attr_qual_name(node.value, aliases)}.{node.attr}"
        if name in aliases:
            return aliases[name]
        return name
    else:
        return ""

