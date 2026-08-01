
def format_type_inner(
    typ: Type,
    verbosity: int,
    options: Options,
    fullnames: set[str] | None,
    module_names: bool = False,
    use_pretty_callable: bool = True,
) -> str:
    """
    Convert a type to a relatively short string suitable for error messages.

    Args:
      typ: type to be formatted
      verbosity: a coarse grained control on the verbosity of the type
      options: Options object controlling formatting
      fullnames: a set of names that should be printed in full
      module_names: whether to show module names for module types
      use_pretty_callable: use pretty_callable to format Callable types.
    """

    def format(typ: Type) -> str:
        return format_type_inner(typ, verbosity, options, fullnames)

    def format_list(types: Sequence[Type]) -> str:
        return ", ".join(format(typ) for typ in types)

    def format_union_items(types: Sequence[Type]) -> list[str]:
        formatted = [format(typ) for typ in types if format(typ) != "None"]
        if len(formatted) > MAX_UNION_ITEMS and verbosity == 0:
            more = len(formatted) - MAX_UNION_ITEMS // 2
            formatted = formatted[: MAX_UNION_ITEMS // 2]
        else:
            more = 0
        if more:
            formatted.append(f"<{more} more items>")
        if any(format(typ) == "None" for typ in types):
            formatted.append("None")
        return formatted

    def format_union(types: Sequence[Type]) -> str:
        return " | ".join(format_union_items(types))

    def format_literal_value(typ: LiteralType) -> str:
        if typ.is_enum_literal():
            underlying_type = format(typ.fallback)
            return f"{underlying_type}.{typ.value}"
        else:
            return typ.value_repr()

    if isinstance(typ, TypeAliasType) and typ.is_recursive:
        if typ.alias is None:
            type_str = "<alias (unfixed)>"
        else:
            if verbosity >= 2 or (fullnames and typ.alias.fullname in fullnames):
                type_str = typ.alias.fullname
            else:
                type_str = typ.alias.name
            if typ.args:
                type_str += f"[{format_list(typ.args)}]"
        return type_str

    # TODO: always mention type alias names in errors.
    typ = get_proper_type(typ)

    if isinstance(typ, Instance):
        itype = typ
        # Get the short name of the type.
        if itype.type.fullname == "types.ModuleType":
            # Make some common error messages simpler and tidier.
            base_str = "Module"
            if itype.extra_attrs and itype.extra_attrs.mod_name and module_names:
                return f'{base_str} "{itype.extra_attrs.mod_name}"'
            return base_str
        if itype.type.fullname == "typing._SpecialForm":
            # This is not a real type but used for some typing-related constructs.
            return "<typing special form>"
        if verbosity >= 2 or (fullnames and itype.type.fullname in fullnames):
            base_str = itype.type.fullname
        else:
            base_str = itype.type.name
        if not itype.args:
            if itype.type.has_type_var_tuple_type and len(itype.type.type_vars) == 1:
                return base_str + "[()]"
            # No type arguments, just return the type name
            return base_str
        elif itype.type.fullname == "builtins.tuple":
            item_type_str = format(itype.args[0])
            return f"tuple[{item_type_str}, ...]"
        else:
            # There are type arguments. Convert the arguments to strings.
            return f"{base_str}[{format_list(itype.args)}]"
    elif isinstance(typ, UnpackType):
        if options.use_star_unpack():
            return f"*{format(typ.type)}"
        return f"Unpack[{format(typ.type)}]"
    elif isinstance(typ, TypeVarType):
        # This is similar to non-generic instance types.
        fullname = scoped_type_var_name(typ)
        if verbosity >= 2 or (fullnames and fullname in fullnames):
            return fullname
        return typ.name
    elif isinstance(typ, TypeVarTupleType):
        # This is similar to non-generic instance types.
        fullname = scoped_type_var_name(typ)
        if verbosity >= 2 or (fullnames and fullname in fullnames):
            return fullname
        return typ.name
    elif isinstance(typ, ParamSpecType):
        # Concatenate[..., P]
        if typ.prefix.arg_types:
            args = format_callable_args(
                typ.prefix.arg_types, typ.prefix.arg_kinds, typ.prefix.arg_names, format, verbosity
            )

            return f"[{args}, **{typ.name_with_suffix()}]"
        else:
            # TODO: better disambiguate ParamSpec name clashes.
            return typ.name_with_suffix()
    elif isinstance(typ, TupleType):
        # Prefer the name of the fallback class (if not tuple), as it's more informative.
        if typ.partial_fallback.type.fullname != "builtins.tuple":
            return format(typ.partial_fallback)
        type_items = format_list(typ.items) or "()"
        return f"tuple[{type_items}]"
    elif isinstance(typ, TypedDictType):
        # If the TypedDictType is named, return the name
        if not typ.is_anonymous():
            return format(typ.fallback)
        items = []
        for item_name, item_type in typ.items.items():
            modifier = ""
            if item_name not in typ.required_keys:
                modifier += "?"
            if item_name in typ.readonly_keys:
                modifier += "="
            items.append(f"{item_name!r}{modifier}: {format(item_type)}")
        return f"TypedDict({{{', '.join(items)}}})"
    elif isinstance(typ, LiteralType):
        return f"Literal[{format_literal_value(typ)}]"
    elif isinstance(typ, UnionType):
        typ = get_proper_type(ignore_last_known_values(typ))
        if not isinstance(typ, UnionType):
            return format(typ)
        literal_items, union_items = separate_union_literals(typ)

        # Coalesce multiple Literal[] members. This also changes output order.
        # If there's just one Literal item, retain the original ordering.
        if len(literal_items) > 1:
            literal_str = "Literal[{}]".format(
                ", ".join(format_literal_value(t) for t in literal_items)
            )

            if len(union_items) == 1 and isinstance(get_proper_type(union_items[0]), NoneType):
                return f"{literal_str} | None"
            elif union_items:
                return f"{literal_str} | {format_union(union_items)}"
            else:
                return literal_str
        else:
            # Only print Union as Optional if the Optional wouldn't have to contain another Union
            print_as_optional = (
                len(typ.items) - sum(isinstance(get_proper_type(t), NoneType) for t in typ.items)
                == 1
            )
            if print_as_optional:
                rest = [t for t in typ.items if not isinstance(get_proper_type(t), NoneType)]
                return f"{format(rest[0])} | None"
            else:
                s = format_union(typ.items)
            return s
    elif isinstance(typ, NoneType):
        return "None"
    elif isinstance(typ, AnyType):
        return "Any"
    elif isinstance(typ, DeletedType):
        return "<deleted>"
    elif isinstance(typ, UninhabitedType):
        return "Never"
    elif isinstance(typ, TypeType):
        if typ.is_type_form:
            type_name = "TypeForm"
        else:
            type_name = "type"
        return f"{type_name}[{format(typ.item)}]"
    elif isinstance(typ, FunctionLike):
        func = typ
        if func.is_type_obj():
            return format(TypeType.make_normalized(func.items[0].get_instance_type()))
        elif isinstance(func, CallableType):
            if func.type_guard is not None:
                return_type = f"TypeGuard[{format(func.type_guard)}]"
            elif func.type_is is not None:
                return_type = f"TypeIs[{format(func.type_is)}]"
            else:
                return_type = format(func.ret_type)
            if func.is_ellipsis_args:
                return f"Callable[..., {return_type}]"
            param_spec = func.param_spec()
            if param_spec is not None:
                return f"Callable[{format(param_spec)}, {return_type}]"

            # Use pretty format (def-style) for complex signatures with named, optional, or star args.
            # Use compact Callable[[...], ...] only for signatures with all simple positional args.
            if use_pretty_callable:
                if any(
                    not should_format_arg_as_type(kind, name, verbosity)
                    for kind, name in zip(func.arg_kinds, func.arg_names)
                ):
                    return pretty_callable(func, options)

            args = format_callable_args(
                func.arg_types, func.arg_kinds, func.arg_names, format, verbosity
            )
            return f"Callable[[{args}], {return_type}]"
        else:
            # Use a simple representation for function types; proper
            # function types may result in long and difficult-to-read
            # error messages.
            return "overloaded function"
    elif isinstance(typ, UnboundType):
        return typ.accept(TypeStrVisitor(options=options))
    elif isinstance(typ, Parameters):
        args = format_callable_args(typ.arg_types, typ.arg_kinds, typ.arg_names, format, verbosity)
        return f"[{args}]"
    elif typ is None:
        raise RuntimeError("Type is None")
    else:
        # Default case; we simply have to return something meaningful here.
        return "object"

