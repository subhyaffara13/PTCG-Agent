
def format_type_distinctly(*types: Type, options: Options, bare: bool = False) -> tuple[str, ...]:
    """Jointly format types to distinct strings.

    Increase the verbosity of the type strings until they become distinct
    while also requiring that distinct types with the same short name are
    formatted distinctly.

    By default, the returned strings are created using format_type() and will be
    quoted accordingly. If ``bare`` is True, the returned strings will not
    be quoted; callers who need to do post-processing of the strings before
    quoting them (such as prepending * or **) should use this.
    """
    overlapping = find_type_overlaps(*types)

    def format_single(arg: Type) -> str:
        return format_type_inner(arg, verbosity=0, options=options, fullnames=overlapping)

    min_verbosity = 0
    # Prevent emitting weird errors like:
    # ... has incompatible type "Callable[[int], Child]"; expected "Callable[[int], Parent]"
    if len(types) == 2:
        left, right = types
        left = get_proper_type(left)
        right = get_proper_type(right)
        # If the right type has named arguments, they may be the reason for incompatibility.
        # This excludes cases when right is Callable[[Something], None] without named args,
        # because that's usually the right thing to do.
        if (
            isinstance(left, CallableType)
            and isinstance(right, CallableType)
            and any(right.arg_names)
            and is_subtype(left, right, ignore_pos_arg_names=True)
        ):
            min_verbosity = 1

    for verbosity in range(min_verbosity, 2):
        strs = [
            format_type_inner(type, verbosity=verbosity, options=options, fullnames=overlapping)
            for type in types
        ]
        if len(set(strs)) == len(strs):
            break
    if bare:
        return tuple(strs)
    else:
        return tuple(quote_type_string(s) for s in strs)

