
def _is_trivial_super_delegation(function: nodes.FunctionDef) -> bool:
    """Check whether a function definition is a method consisting only of a
    call to the same function on the superclass.
    """
    if (
        not function.is_method()
        # Adding decorators to a function changes behavior and
        # constitutes a non-trivial change.
        or function.decorators
    ):
        return False

    body = function.body
    if len(body) != 1:
        # Multiple statements, which means this overridden method
        # could do multiple things we are not aware of.
        return False

    statement = body[0]
    if not isinstance(statement, (nodes.Expr, nodes.Return)):
        # Doing something else than what we are interested in.
        return False

    call = statement.value
    match call := statement.value:
        case nodes.Call(func=nodes.Attribute(expr=expr)):
            pass
        case _:
            # Not a super() attribute access.
            return False

    # Anything other than a super call is non-trivial.
    super_call = safe_infer(expr)
    if not isinstance(super_call, objects.Super):
        return False

    # The name should be the same.
    if call.func.attrname != function.name:
        return False

    # Should be a super call with the MRO pointer being the
    # current class and the type being the current instance.
    current_scope = function.parent.scope()
    if not (
        super_call.mro_pointer == current_scope
        and isinstance(super_call.type, astroid.Instance)
        and super_call.type.name == current_scope.name
    ):
        return False

    return True

