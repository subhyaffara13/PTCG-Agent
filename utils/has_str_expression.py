
def has_str_expression(node: Expression) -> bool:
    v = StringSeeker()
    node.accept(v)
    return v.found

