
def _is_typing(node, typing_attr, scope_stack):
    """
    Determine whether `node` represents the member of a typing module specified
    by `typing_attr`.

    This is used as part of working out whether we are within a type annotation
    context.
    """
    return _is_typing_helper(node, lambda x: x == typing_attr, scope_stack)

