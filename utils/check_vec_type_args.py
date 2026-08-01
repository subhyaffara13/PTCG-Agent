
def check_vec_type_args(
    args: tuple[Type, ...] | list[Type], ctx: Context, api: SemanticAnalyzerCoreInterface
) -> bool:
    """Report an error if type args for 'vec' are invalid.

    Return False on error.
    """
    ok = True
    if len(args) != 1:
        ok = False
    else:
        arg = get_proper_type(args[0])
        if isinstance(arg, Instance):
            if arg.type.fullname == "builtins.int":
                # A fixed-width integer such as 'i64' must be used instead of plain 'int'
                ok = False
        elif isinstance(arg, UnionType):
            non_optional = None
            items = [get_proper_type(item) for item in arg.items]
            if len(items) != 2:
                ok = False
            elif isinstance(items[0], NoneType):
                if not check_vec_type_args([items[1]], ctx, api):
                    # Error has already been reported so it's fine to return
                    return False
                non_optional = items[1]
            elif isinstance(items[1], NoneType):
                if not check_vec_type_args([items[0]], ctx, api):
                    # Error has already been reported so it's fine to return
                    return False
                non_optional = items[0]
            else:
                ok = False
            if isinstance(non_optional, Instance) and (
                non_optional.type.fullname in MYPYC_NATIVE_INT_NAMES
                or non_optional.type.fullname
                in ("builtins.int", "builtins.float", "builtins.bool", "librt.vecs.vec")
            ):
                ok = False
        elif isinstance(arg, TypeVarType):
            # Generic vec types aren't supported in type checked Python code, but
            # they can be provided in libraries implemented in C (e.g. append).
            if not api.is_stub_file:
                ok = False
        else:
            ok = False
    if not ok:
        api.fail('Invalid item type for "vec"', ctx)
    return ok

