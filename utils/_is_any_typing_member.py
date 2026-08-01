
def _is_any_typing_member(node, scope_stack):
    """
    Determine whether `node` represents any member of a typing module.

    This is used as part of working out whether we are within a type annotation
    context.
    """
    return _is_typing_helper(node, lambda x: True, scope_stack)

