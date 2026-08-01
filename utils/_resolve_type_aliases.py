
def _resolve_type_aliases(field_type: typing.Any) -> typing.Any:
    # Recursively resolve PEP 695 (`type X = ...`) type aliases (Python
    # 3.12+) to their underlying value, so that the rest of the
    # normalization logic never encounters an alias. Aliases can refer
    # to other aliases and can appear at any level of nesting (e.g.
    # inside `Annotated[...]`, unions, or `list[...]`).
    if sys.version_info < (3, 12):
        return field_type

    while isinstance(field_type, typing.TypeAliasType):
        field_type = field_type.__value__

    args = typing.get_args(field_type)
    resolved_args = tuple(_resolve_type_aliases(arg) for arg in args)
    if resolved_args == args:
        # No aliases anywhere inside: return the type unchanged.
        return field_type

    if _is_union(field_type):
        # `X | Y` unions can't be rebuilt through their origin like
        # other generics below: `typing.get_origin` returns
        # `types.UnionType` for them, which is only subscriptable on
        # Python 3.14+. Rebuilding through `typing.Union` also
        # flattens any nested union introduced by an alias of a union
        # (e.g. `Time | int` where `type Time = UTCTime |
        # GeneralizedTime`), just like `typing.Union` would have done
        # if the alias had been written inline.
        return typing.Union[resolved_args]

    # An alias appeared inside a generic (e.g. `Annotated[Time, ...]`,
    # `list[MyInt]`, or `SetOf[MyInt]`): re-parameterize the generic
    # with the resolved arguments. Subscripting with a tuple is
    # equivalent to subscripting with multiple arguments.
    return typing.get_origin(field_type)[resolved_args]

