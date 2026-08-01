
def _determine_callable(
    callable_obj: nodes.NodeNG,
) -> tuple[CallableObjects, int, str]:
    # TODO: The typing of the second return variable is actually Literal[0,1]
    # We need typing on nodes.NodeNG.implicit_parameters for this
    # TODO: The typing of the third return variable can be narrowed to a Literal
    # We need typing on nodes.NodeNG.type for this

    # Ordering is important, since BoundMethod is a subclass of UnboundMethod,
    # and Function inherits Lambda.
    parameters = 0
    if hasattr(callable_obj, "implicit_parameters"):
        parameters = callable_obj.implicit_parameters()
    match callable_obj:
        case bases.BoundMethod():
            # Bound methods have an extra implicit 'self' argument.
            return callable_obj, parameters, callable_obj.type
        case bases.UnboundMethod():
            return callable_obj, parameters, "unbound method"
        case nodes.FunctionDef():
            return callable_obj, parameters, callable_obj.type
        case nodes.Lambda():
            return callable_obj, parameters, "lambda"
        case nodes.ClassDef():
            # Class instantiation, Check first for a metaclass __call__ definition.
            # Then lookup __new__. If we only find object.__new__,
            # we can safely check __init__ instead.
            # If __new__ belongs to builtins, then we look
            # again for __init__ in the locals, since we won't have
            # argument information for the builtin __new__ function.

            # Try to use the metaclass' __call__ if any.
            meta = callable_obj.metaclass()
            if isinstance(meta, nodes.ClassDef):
                meta_call, _, from_builtins = _get_local_callable(meta, "__call__")
                if meta_call and not from_builtins:
                    _check_is_function_def(meta_call)
                    return meta_call, parameters, "class"

            # Use the last definition of __new__.
            new, from_object, from_builtins = _get_local_callable(
                callable_obj, "__new__"
            )
            if not new or from_object or from_builtins:
                try:
                    # Use the last definition of __init__.
                    callable_obj = callable_obj.local_attr("__init__")[-1]
                except astroid.NotFoundError as e:
                    raise ValueError from e
            else:
                callable_obj = new

            _check_is_function_def(callable_obj)
            return callable_obj, parameters, "constructor"

    raise ValueError

