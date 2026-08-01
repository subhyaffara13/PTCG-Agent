
def refers_to_class_or_function(node: Expression) -> bool:
    """Does semantically analyzed node refer to a class?"""
    return isinstance(node, RefExpr) and isinstance(
        node.node, (TypeInfo, FuncDef, OverloadedFuncDef)
    )

