
def _verify_arg_default_value(
    stub_arg: nodes.Argument, runtime_arg: inspect.Parameter
) -> Iterator[str]:
    """Checks whether argument default values are compatible."""
    if runtime_arg.default is not inspect.Parameter.empty:
        if stub_arg.kind.is_required():
            yield (
                f'runtime parameter "{runtime_arg.name}" '
                "has a default value but stub parameter does not"
            )
        else:
            type_context = stub_arg.variable.type
            runtime_type = get_mypy_type_of_runtime_value(
                runtime_arg.default, type_context=type_context
            )

            # Fallback to the type annotation type if var type is missing. The type annotation
            # is an UnboundType, but I don't know enough to know what the pros and cons here are.
            # UnboundTypes have ugly question marks following them, so default to var type.
            # Note we do this same fallback when constructing signatures in from_overloadedfuncdef
            stub_type = stub_arg.variable.type or stub_arg.type_annotation
            if isinstance(stub_type, mypy.types.TypeVarType):
                stub_type = stub_type.upper_bound
            if (
                runtime_type is not None
                and stub_type is not None
                # Avoid false positives for marker objects
                and type(runtime_arg.default) is not object
                # And ellipsis
                and runtime_arg.default is not ...
                and not is_subtype_helper(runtime_type, stub_type)
            ):
                yield (
                    f'runtime parameter "{runtime_arg.name}" '
                    f"has a default value of type {runtime_type}, "
                    f"which is incompatible with stub parameter type {stub_type}"
                )
            if stub_arg.initializer is not None:
                stub_default = evaluate_expression(stub_arg.initializer)
                if (
                    stub_default is not UNKNOWN
                    and stub_default is not ...
                    and runtime_arg.default is not UNREPRESENTABLE
                ):
                    defaults_match = True
                    # We want the types to match exactly, e.g. in case the stub has
                    # True and the runtime has 1 (or vice versa).
                    if type(stub_default) is not type(runtime_arg.default):
                        defaults_match = False
                    else:
                        try:
                            defaults_match = bool(stub_default == runtime_arg.default)
                        except Exception:
                            # Exception can be raised in bool dunder method (e.g. numpy arrays)
                            # At this point, consider the default to be different, it is probably
                            # too complex to put in a stub anyway.
                            defaults_match = False
                    if not defaults_match:
                        yield (
                            f'runtime parameter "{runtime_arg.name}" '
                            f"has a default value of {runtime_arg.default!r}, "
                            f"which is different from stub parameter default {stub_default!r}"
                        )
    else:
        if stub_arg.kind.is_optional():
            yield (
                f'stub parameter "{stub_arg.variable.name}" has a default value '
                f"but runtime parameter does not"
            )

