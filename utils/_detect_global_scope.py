
def _detect_global_scope(
    node: nodes.Name,
    frame: nodes.LocalsDictNodeNG,
    defframe: nodes.LocalsDictNodeNG,
) -> bool:
    """Detect that the given frames share a global scope.

    Two frames share a global scope when neither
    of them are hidden under a function scope, as well
    as any parent scope of them, until the root scope.
    In this case, depending from something defined later on
    will only work if guarded by a nested function definition.

    Example:
        class A:
            # B has the same global scope as `C`, leading to a NameError.
            # Return True to indicate a shared scope.
            class B(C): ...
        class C: ...

    Whereas this does not lead to a NameError:
        class A:
            def guard():
                # Return False to indicate no scope sharing.
                class B(C): ...
        class C: ...
    """
    if defframe.lineno is None:
        # ``defframe`` is a synthetic node, such as a dataclass-generated
        # ``__init__``, so it has no source position to order against.
        return False
    def_scope = scope = None
    if frame and frame.parent:
        scope = frame.parent.scope()
    if defframe and defframe.parent:
        def_scope = defframe.parent.scope()
    if (
        isinstance(frame, nodes.ClassDef)
        and scope is not def_scope
        and scope is utils.get_node_first_ancestor_of_type(node, nodes.FunctionDef)
    ):
        # If the current node's scope is a class nested under a function,
        # and the def_scope is something else, then they aren't shared.
        return False
    if isinstance(frame, nodes.FunctionDef):
        # If the parent of the current node is a
        # function, then it can be under its scope (defined in); or
        # the `->` part of annotations. The same goes
        # for annotations of function arguments, they'll have
        # their parent the Arguments node.
        if frame.parent_of(defframe):
            return node.lineno < defframe.lineno  # type: ignore[no-any-return]
        if not isinstance(node.parent, (nodes.FunctionDef, nodes.Arguments)):
            return False

    break_scopes = []
    for current_scope in (scope or frame, def_scope):
        # Look for parent scopes. If there is anything different
        # than a module or a class scope, then the frames don't
        # share a global scope.
        parent_scope = current_scope
        while parent_scope:
            if not isinstance(parent_scope, (nodes.ClassDef, nodes.Module)):
                break_scopes.append(parent_scope)
                break
            if parent_scope.parent:
                parent_scope = parent_scope.parent.scope()
            else:
                break
    if len(set(break_scopes)) > 1:
        # Store different scopes than expected.
        # If the stored scopes are, in fact, the very same, then it means
        # that the two frames (frame and defframe) share the same scope,
        # and we could apply our lineno analysis over them.
        # For instance, this works when they are inside a function, the node
        # that uses a definition and the definition itself.
        return False
    # At this point, we are certain that frame and defframe share a scope
    # and the definition of the first depends on the second.
    return frame.lineno < defframe.lineno  # type: ignore[no-any-return]

