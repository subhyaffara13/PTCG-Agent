from typing import Any

def get_mypy_type_of_runtime_value(
    runtime: Any, type_context: mypy.types.Type | None = None
) -> mypy.types.Type | None:
    """Returns a mypy type object representing the type of ``runtime``.

    Returns None if we can't find something that works.

    """
    if runtime is None:
        return mypy.types.NoneType()
    if isinstance(runtime, property):
        # Give up on properties to avoid issues with things that are typed as attributes.
        return None

    def anytype() -> mypy.types.AnyType:
        return mypy.types.AnyType(mypy.types.TypeOfAny.unannotated)

    if isinstance(
        runtime,
        (types.FunctionType, types.BuiltinFunctionType, types.MethodType, types.BuiltinMethodType),
    ):
        builtins = get_stub("builtins")
        assert builtins is not None
        type_info = builtins.names["function"].node
        assert isinstance(type_info, nodes.TypeInfo)
        fallback = mypy.types.Instance(type_info, [anytype()])
        signature = safe_inspect_signature(runtime)
        if signature:
            arg_types = []
            arg_kinds = []
            arg_names = []
            for arg in signature.parameters.values():
                arg_types.append(anytype())
                arg_names.append(
                    None if arg.kind == inspect.Parameter.POSITIONAL_ONLY else arg.name
                )
                no_default = arg.default is inspect.Parameter.empty
                if arg.kind == inspect.Parameter.POSITIONAL_ONLY:
                    arg_kinds.append(nodes.ARG_POS if no_default else nodes.ARG_OPT)
                elif arg.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                    arg_kinds.append(nodes.ARG_POS if no_default else nodes.ARG_OPT)
                elif arg.kind == inspect.Parameter.KEYWORD_ONLY:
                    arg_kinds.append(nodes.ARG_NAMED if no_default else nodes.ARG_NAMED_OPT)
                elif arg.kind == inspect.Parameter.VAR_POSITIONAL:
                    arg_kinds.append(nodes.ARG_STAR)
                elif arg.kind == inspect.Parameter.VAR_KEYWORD:
                    arg_kinds.append(nodes.ARG_STAR2)
                else:
                    raise AssertionError
        else:
            arg_types = [anytype(), anytype()]
            arg_kinds = [nodes.ARG_STAR, nodes.ARG_STAR2]
            arg_names = [None, None]

        return mypy.types.CallableType(
            arg_types,
            arg_kinds,
            arg_names,
            ret_type=anytype(),
            fallback=fallback,
            is_ellipsis_args=True,
        )

    skip_type_object_type = False
    if type_context:
        # Don't attempt to process the type object when context is generic
        # This is related to issue #3737
        type_context = mypy.types.get_proper_type(type_context)
        # Callable types with a generic return value
        if isinstance(type_context, mypy.types.CallableType):
            if isinstance(type_context.ret_type, mypy.types.TypeVarType):
                skip_type_object_type = True
        # Type[x] where x is generic
        if isinstance(type_context, mypy.types.TypeType):
            if isinstance(type_context.item, mypy.types.TypeVarType):
                skip_type_object_type = True

    if isinstance(runtime, type) and not skip_type_object_type:
        # Try and look up a stub for the runtime object itself
        # The logic here is similar to ExpressionChecker.analyze_ref_expr
        type_info = get_mypy_node_for_name(runtime.__module__, runtime.__name__)
        if isinstance(type_info, nodes.TypeInfo):
            result = mypy.typeops.type_object_type(type_info)
            if mypy.checkexpr.is_type_type_context(type_context):
                # This is the type in a type[] expression, so substitute type
                # variables with Any.
                result = mypy.erasetype.erase_typevars(result)
            return result

    # Try and look up a stub for the runtime object's type
    type_info = get_mypy_node_for_name(type(runtime).__module__, type(runtime).__name__)
    if type_info is None:
        return None
    if isinstance(type_info, nodes.Var):
        return type_info.type
    if not isinstance(type_info, nodes.TypeInfo):
        return None

    if isinstance(runtime, tuple):
        # Special case tuples so we construct a valid mypy.types.TupleType
        optional_items = [get_mypy_type_of_runtime_value(v) for v in runtime]
        items = [(i if i is not None else anytype()) for i in optional_items]
        fallback = mypy.types.Instance(type_info, [anytype()])
        return mypy.types.TupleType(items, fallback)

    fallback = mypy.types.Instance(type_info, [anytype() for _ in type_info.type_vars])
    if type(runtime) != runtime.__class__:
        # Since `__class__` is redefined for an instance, we can't trust
        # its `isinstance` checks, it can be dynamic. See #20919
        return fallback

    value: bool | int | str
    if isinstance(runtime, enum.Enum) and isinstance(runtime.name, str):
        value = runtime.name
    elif isinstance(runtime, bytes):
        value = bytes_to_human_readable_repr(runtime)
    elif isinstance(runtime, (bool, int, str)):
        value = runtime
    else:
        return fallback

    return mypy.types.LiteralType(value=value, fallback=fallback)

