
def pretty_callable(tp: CallableType, options: Options, skip_self: bool = False) -> str:
    """Return a nice easily-readable representation of a callable type.
    For example:
        def [T <: int] f(self, x: int, y: T) -> None

    If skip_self is True, print an actual callable type, as it would appear
    when bound on an instance/class, rather than how it would appear in the
    defining statement.
    """
    s = ""
    asterisk = False
    slash = False
    for i in range(len(tp.arg_types)):
        if s:
            s += ", "
        if tp.arg_kinds[i].is_named() and not asterisk:
            s += "*, "
            asterisk = True
        if tp.arg_kinds[i] == ARG_STAR:
            s += "*"
            asterisk = True
        if tp.arg_kinds[i] == ARG_STAR2:
            s += "**"
        name = tp.arg_names[i]
        if not name and not options.reveal_verbose_types:
            # Avoid ambiguous (and weird) formatting for anonymous args/kwargs.
            if tp.arg_kinds[i] == ARG_STAR and isinstance(tp.arg_types[i], UnpackType):
                name = "args"
            elif tp.arg_kinds[i] == ARG_STAR2 and tp.unpack_kwargs:
                name = "kwargs"
        if name:
            s += name + ": "
        type_str = format_type_bare(tp.arg_types[i], options)
        if tp.arg_kinds[i] == ARG_STAR2 and tp.unpack_kwargs:
            if options.reveal_verbose_types:
                type_str = f"Unpack[{type_str}]"
            else:
                type_str = f"**{type_str}"
        s += type_str
        if tp.arg_kinds[i].is_optional():
            s += " = ..."
        if (
            not slash
            and tp.arg_kinds[i].is_positional()
            and name is None
            and (
                i == len(tp.arg_types) - 1
                or (tp.arg_names[i + 1] is not None or not tp.arg_kinds[i + 1].is_positional())
            )
        ):
            s += ", /"
            slash = True

    definition = get_func_def(tp)

    # Extract function name, prefer the "human-readable" name if available.
    func_name = None
    if tp.name:
        func_name = tp.name.split()[0]  # skip "of Class" part
    elif isinstance(definition, FuncDef):
        func_name = definition.name

    # If we got a "special arg" (i.e: self, cls, etc...), prepend it to the arg list
    first_arg = None
    if (
        isinstance(definition, FuncDef)
        and hasattr(definition, "arguments")
        and not tp.from_concatenate
    ):
        definition_arg_names = [arg.variable.name for arg in definition.arguments]
        if len(definition_arg_names) > len(tp.arg_names) and definition_arg_names[0]:
            first_arg = definition_arg_names[0]
    else:
        # TODO: avoid different logic for incremental runs.
        first_arg = get_first_arg(tp)

    if tp.is_type_obj():
        skip_self = True
    if first_arg and not skip_self:
        if s:
            s = ", " + s
        s = first_arg + s
    if func_name:
        s = f"{func_name}({s})"
    else:
        s = f"({s})"

    s += " -> "
    if tp.type_guard is not None:
        s += f"TypeGuard[{format_type_bare(tp.type_guard, options)}]"
    elif tp.type_is is not None:
        s += f"TypeIs[{format_type_bare(tp.type_is, options)}]"
    else:
        s += format_type_bare(tp.ret_type, options)

    if tp.variables:
        tvars = []
        for tvar in tp.variables:
            if isinstance(tvar, TypeVarType):
                upper_bound = get_proper_type(tvar.upper_bound)
                if not (
                    isinstance(upper_bound, Instance)
                    and upper_bound.type.fullname == "builtins.object"
                ):
                    tvars.append(f"{tvar.name}: {format_type_bare(upper_bound, options)}")
                elif tvar.values:
                    tvars.append(
                        "{}: ({})".format(
                            tvar.name,
                            ", ".join([format_type_bare(tp, options) for tp in tvar.values]),
                        )
                    )
                else:
                    tvars.append(tvar.name)
            else:
                # For other TypeVarLikeTypes, just use the repr
                tvars.append(repr(tvar))
        s = f"[{', '.join(tvars)}] {s}"
    return f"def {s}"

