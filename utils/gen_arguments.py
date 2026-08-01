
def gen_arguments(
    flat_arguments: Sequence[Argument], skipped_args: set[str]
) -> tuple[list[str], list[str]]:
    types: list[str] = []
    new_names: list[str] = []
    callsite_exprs: list[str] = []
    for arg in flat_arguments:
        if arg.name in skipped_args:
            # Pass the arg's schema default when available (e.g. "false" for
            # a bool arg with default=False), so non-optional args with defaults
            # can be versioned too. Fall back to std::nullopt for optional args
            # with no default (matches historical behavior).
            if arg.default is not None:
                from torchgen.api.cpp import default_expr

                callsite_exprs.append(default_expr(arg.default, arg.type, symint=False))
            else:
                callsite_exprs.append("std::nullopt")
            continue
        new_types, names, _, new_callsite_exprs = convert_arg_type_and_name(
            arg.type, arg.name, arg.is_write
        )
        types.extend(new_types)
        new_names.extend(names)
        callsite_exprs.extend(new_callsite_exprs)
    return zip_type_and_name(types, new_names), callsite_exprs

