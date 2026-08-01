
def make_inferred_type_note(
    context: Context, subtype: Type, supertype: Type, supertype_str: str
) -> str:
    """Explain that the user may have forgotten to type a variable.

    The user does not expect an error if the inferred container type is the same as the return
    type of a function and the argument type(s) are a subtype of the argument type(s) of the
    return type. This note suggests that they add a type annotation with the return type instead
    of relying on the inferred type.
    """
    subtype = get_proper_type(subtype)
    supertype = get_proper_type(supertype)
    if (
        isinstance(subtype, Instance)
        and isinstance(supertype, Instance)
        and subtype.type.fullname == supertype.type.fullname
        and subtype.args
        and supertype.args
        and isinstance(context, ReturnStmt)
        and isinstance(context.expr, NameExpr)
        and isinstance(context.expr.node, Var)
        and context.expr.node.is_inferred
    ):
        for subtype_arg, supertype_arg in zip(subtype.args, supertype.args):
            if not is_subtype(subtype_arg, supertype_arg):
                return ""
        var_name = context.expr.name
        return 'Perhaps you need a type annotation for "{}"? Suggestion: {}'.format(
            var_name, supertype_str
        )
    return ""

